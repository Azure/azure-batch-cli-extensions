# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.pipeline import ClientRawResponse
from azure.batch.operations.task_operations import TaskOperations

from .. import models


MAX_TASKS_PER_REQUEST = 100


class ExtendedTaskOperations(TaskOperations):
    """PoolOperations operations.

    :param parent: The parent BatchExtensionsClient object.
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :param get_storage_account: A callable to retrieve a storage client object.
    """
    def __init__(self, parent, client, config, serializer, deserializer, get_storage_account):
        super(ExtendedTaskOperations, self).__init__(client, config, serializer, deserializer)
        self._parent = parent
        self.get_storage_client = get_storage_account

    def _bulk_add_tasks(self, queue, *args, **kwargs):
        try:
            added_tasks = super(ExtendedTaskOperations, self).add_collection(*args, **kwargs)
        except Exception as exp:  # pylint: disable=broad-except
            queue.put(exp)
        else:
            if isinstance(added_tasks, ClientRawResponse):
                for task in added_tasks.output.value:
                    queue.put(task)
            else:
                for task in added_tasks.value:  # pylint: disable=no-member
                    queue.put(task)

    def add_collection(
            self, job_id, value, task_add_collection_options=None, custom_headers=None, raw=False):
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
        submitted_tasks = []
        if self._parent.threads:
            import threading
            try:
                import queue
            except ImportError:
                import Queue as queue
            start = 0
            task_queue = queue.Queue()
            submitting_tasks = []
            while True:
                end = min(start + MAX_TASKS_PER_REQUEST, len(value))
                submitting_tasks.append(threading.Thread(
                    target=self._bulk_add_tasks,
                    args=(task_queue,
                          job_id,
                          value[start:end],
                          task_add_collection_options,
                          custom_headers,
                          raw)))
                submitting_tasks[-1].start()
                start = end
                error = None
                if start >= len(value) or len(submitting_tasks) >= self._parent.threads:
                    while any(s for s in submitting_tasks if s.is_alive()) or not task_queue.empty():
                        queued = task_queue.get()
                        task_queue.task_done()
                        if isinstance(queued, Exception):
                            error = queued
                        else:
                            submitted_tasks.append(queued)
                    if error:
                        raise error  # pylint: disable=raising-bad-type
                    if start >= len(value):
                        break
        else:
            for i in range(0, len(value), MAX_TASKS_PER_REQUEST):
                submission = super(ExtendedTaskOperations, self).add_collection(
                    job_id,
                    value[i:i + MAX_TASKS_PER_REQUEST],
                    task_add_collection_options,
                    custom_headers,
                    raw)
                if isinstance(submission, ClientRawResponse):
                    submitted_tasks.extend(submission.output.value)
                else:
                    submitted_tasks.extend(submission.value)  # pylint: disable=no-member
        return models.TaskAddCollectionResult(value=submitted_tasks)
    add_collection.metadata = {'url': '/jobs/{jobId}/addtaskcollection'}
