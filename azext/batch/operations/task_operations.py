# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import collections
import logging
import threading

from azure.batch.models import BatchErrorException
from azure.batch.models.batch_service_client_enums import TaskAddStatus
from azure.batch.operations.task_operations import TaskOperations
from msrest.pipeline import ClientRawResponse
from .. import errors
from .. import models


class ExtendedTaskOperations(TaskOperations):
    """TaskOperations operations.

    :param parent: The parent BatchExtensionsClient object.
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An object model deserializer.
    :param get_storage_account: A callable to retrieve a storage client object.
    """

    MAX_TASKS_PER_REQUEST = 100

    def __init__(self, parent, client, config, serializer, deserializer, get_storage_account):
        super(ExtendedTaskOperations, self).__init__(client, config, serializer, deserializer)
        self._parent = parent
        self.get_storage_client = get_storage_account

    class _TaskWorkflowManager(object):
        """Worker class for one add_collection request

        :param ExtendedTaskOperations task_operations: Parent object which instantiated this
        :param job_id: The ID of the job to which the task collection is to be
         added.
        :type job_id: str
        :param value: The collection of tasks to add.
        :type value: list of :class:`TaskAddParameter
         <azure.batch.models.TaskAddParameter>`
        :param task_add_collection_options: Additional parameters for the
         operation
        :type task_add_collection_options: :class:`TaskAddCollectionOptions
         <azure.batch.models.TaskAddCollectionOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        """

        def __init__(
                self,
                task_operations,
                job_id,
                tasks_to_add,
                task_add_collection_options=None,
                custom_headers=None,
                raw=False,
                **kwargs):
            # No complex operations - No lock needed
            self._has_early_termination_error = False

            # Append operations thread safe
            # Only read once all threads have completed
            self._failures = collections.deque()

            # synchronized through lock variables
            self.error = None  # Only written once all threads have completed
            self._max_tasks_per_request = task_operations.MAX_TASKS_PER_REQUEST
            self._tasks_to_add = collections.deque(tasks_to_add)

            self._error_lock = threading.Lock()
            self._max_tasks_lock = threading.Lock()
            self._pending_queue_lock = threading.Lock()

            # Variables to be used for task add_collection requests
            self._task_operations = task_operations
            self._job_id = job_id
            self._task_add_collection_options = task_add_collection_options
            self._custom_headers = custom_headers
            self._raw = raw
            self._kwargs = dict(**kwargs)

        def _bulk_add_tasks(self, results_queue, chunk_tasks_to_add):
            """Adds a chunk of tasks to the job and retry if chunk

            :param results_queue: Queue to place the return value of the request
            :type results_queue: collections.deque
            :param chunk_tasks_to_add: Chunk of at most 100 tasks with retry details
            :type chunk_tasks_to_add: list[~TrackedCloudTask]
            """

            try:
                add_collection_response = super(self._task_operations.__class__, self._task_operations).add_collection(
                    self._job_id,
                    chunk_tasks_to_add,
                    self._task_add_collection_options,
                    self._custom_headers,
                    self._raw)
            except BatchErrorException as e:
                # In case of a chunk exceeding the MaxMessageSize split chunk in half
                # and resubmit smaller chunk requests
                # TODO: Replace string with constant variable once available in SDK
                if e.error.code == "RequestBodyTooLarge":  # pylint: disable=no-member
                    # In this case the task is misbehaved and will not be able to be added due to:
                    #   1) The task exceeding the max message size
                    #   2) A single cell of the task exceeds the per-cell limit, or
                    #   3) Sum of all cells exceeds max row limit
                    if len(chunk_tasks_to_add) == 1:
                        failed_task = chunk_tasks_to_add.pop()
                        results_queue.appendleft(e)
                        logging.error("Task ID " + failed_task.id + " failed to add due to exceeding the request body" +
                                      " being too large")
                        self._has_early_termination_error = True
                    else:
                        # Assumption: Tasks are relatively close in size therefore if one batch exceeds size limit
                        # we should decrease the initial task collection size to avoid repeating the error
                        # Midpoint is lower bounded by 1 due to above base case
                        midpoint = int(len(chunk_tasks_to_add) / 2)
                        # Restrict one thread at a time to do this compare and set,
                        # therefore forcing max_tasks_per_request to be strictly decreasing
                        with self._max_tasks_lock:
                            if midpoint < self._max_tasks_per_request:
                                self._max_tasks_per_request = midpoint
                                logging.info("Amount of tasks per request reduced from " +
                                             str(self._max_tasks_per_request) + " to " + str(midpoint) +
                                             " due to the request body being too large")

                        # Not the most efficient solution for all cases, but the goal of this is to handle this
                        # exception and have it work in all cases where tasks are well behaved
                        # Behavior retries as a smaller chunk and
                        # appends extra tasks to queue to be picked up by another thread .
                        self._tasks_to_add.extendleft(chunk_tasks_to_add[midpoint:])
                        self._bulk_add_tasks(results_queue, chunk_tasks_to_add[:midpoint])
                elif 500 <= e.response.status_code <= 599:
                    self._tasks_to_add.extendleft(chunk_tasks_to_add)
                else:
                    results_queue.appendleft(e)
            except Exception as e:  # pylint: disable=broad-except
                results_queue.appendleft(e)
            else:
                if isinstance(add_collection_response, ClientRawResponse):
                    add_collection_response = add_collection_response.output

                for task_result in add_collection_response.value:  # pylint: disable=no-member
                    if task_result.status == TaskAddStatus.server_error:
                        # Server error will be retried
                        with self._pending_queue_lock:
                            for task in chunk_tasks_to_add:
                                if task.id == task_result.task_id:
                                    self._tasks_to_add.appendleft(task)
                    elif (task_result.status == TaskAddStatus.client_error
                          and not task_result.error.code == "TaskExists"):
                        # Client error will be recorded unless Task already exists
                        self._failures.appendleft(task_result)
                    else:
                        results_queue.appendleft(task_result)

        def task_collection_thread_handler(self, results_queue):
            """Main method for worker to run

            Pops a chunk of tasks off the collection of pending tasks to be added and submits them to be added.

            :param collections.deque results_queue: Queue for worker to output results to
            """
            while len(self._tasks_to_add) != 0 and not self._has_early_termination_error:
                max_tasks = self._max_tasks_per_request  # local copy
                chunk_tasks_to_add = []
                with self._pending_queue_lock:
                    while len(chunk_tasks_to_add) < max_tasks and len(self._tasks_to_add) != 0:
                        chunk_tasks_to_add.append(self._tasks_to_add.pop())

                if len(chunk_tasks_to_add) != 0:
                    self._bulk_add_tasks(results_queue, chunk_tasks_to_add)


            # Only define error if all threads have finished and there were failures
            with self._error_lock:
                if threading.active_count() == 1 and len(self._failures) > 0:
                    self.error = errors.CreateTasksErrorException(
                        "One or more tasks failed to be added",
                        self._failures,
                        self._tasks_to_add)
                else:
                    return

    @staticmethod
    def _handle_output(results_queue):
        """Scan output for exceptions

        If there is an output from an add task collection call add it to the results or throw the respective exception.

        :param results_queue: Queue containing results of attempted add_collection's
        :type results_queue: collections.deque
        :return: list of TaskAddResults
        :rtype: list[~TaskAddResult]
        """
        results = []
        while len(results_queue) != 0:
            queue_item = results_queue.pop()
            if isinstance(queue_item, Exception):
                raise queue_item
            else:
                results.append(queue_item)
        return results

    def add_collection(
            self, job_id, value, task_add_collection_options=None, custom_headers=None, raw=False, threads=None,
            **operation_config):
        """Adds a collection of tasks to the specified job.

        Note that each task must have a unique ID. The Batch service may not
        return the results for each task in the same order the tasks were
        submitted in this request. If the server times out or the connection is
        closed during the request, the request may have been partially or fully
        processed, or not at all. In such cases, the user should re-issue the
        request. Note that it is up to the user to correctly handle failures
        when re-issuing a request. For example, you should use the same task
        IDs during a retry so that if the prior operation succeeded, the retry
        will not create extra tasks unexpectedly. If the response contains any
        tasks which failed to add, a client can retry the request. In a retry,
        it is most efficient to resubmit only tasks that failed to add, and to
        omit tasks that were successfully added on the first attempt. The
        maximum lifetime of a task from addition to completion is 7 days. If a
        task has not completed within 7 days of being added it will be
        terminated by the Batch service and left in whatever state it was in at
        that time.

        :param job_id: The ID of the job to which the task collection is to be
         added.
        :type job_id: str
        :param value: The collection of tasks to add. The total serialized
         size of this collection must be less than 4MB. If it is greater than
         4MB (for example if each task has 100's of resource files or
         environment variables), the request will fail with code
         'RequestBodyTooLarge' and should be retried again with fewer tasks.
        :type value: list of :class:`TaskAddParameter
         <azure.batch.models.TaskAddParameter>`
        :param task_add_collection_options: Additional parameters for the
         operation
        :type task_add_collection_options: :class:`TaskAddCollectionOptions
         <azure.batch.models.TaskAddCollectionOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param int threads: number of threads to use in parallel when adding tasks. If specified
         and greater than 0, will start additional threads to submit requests and wait for them to finish.
         Otherwise will submit add_collection requests sequentially on main thread
        :return: :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises:
         :class:`BatchErrorException<azure.batch.models.BatchErrorException>`
        """

        results_queue = collections.deque()  # deque operations(append/pop) are thread-safe
        task_workflow_manager = self._TaskWorkflowManager(
            self,
            job_id,
            value,
            task_add_collection_options,
            custom_headers,
            raw,
            **operation_config)

        # multi-threaded behavior
        if threads and threads > 0:
            active_threads = []
            for i in range(threads):
                active_threads.append(threading.Thread(
                    target=task_workflow_manager.task_collection_thread_handler,
                    args=(results_queue,)))
                active_threads[i].start()
            for thread in active_threads:
                thread.join()
        # single-threaded behavior
        else:
            task_workflow_manager.task_collection_thread_handler(results_queue)

        submitted_tasks = ExtendedTaskOperations._handle_output(results_queue)
        if task_workflow_manager.error:
            raise task_workflow_manager.error  # pylint: disable=raising-bad-type
        else:
            return models.TaskAddCollectionResult(value=submitted_tasks)
    add_collection.metadata = {'url': '/jobs/{jobId}/addtaskcollection'}
