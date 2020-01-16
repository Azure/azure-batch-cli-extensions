# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class JobPreparationTaskExecutionInformation(Model):
    """Contains information about the execution of a Job Preparation Task on a
    Compute Node.

    All required parameters must be populated in order to send to Azure.

    :param start_time: Required. The time at which the Task started running.
     If the Task has been restarted or retried, this is the most recent time at
     which the Task started running.
    :type start_time: datetime
    :param end_time: The time at which the Job Preparation Task completed.
     This property is set only if the Task is in the Completed state.
    :type end_time: datetime
    :param state: Required. The current state of the Job Preparation Task on
     the Compute Node. Possible values include: 'running', 'completed'
    :type state: str or ~azure.batch.models.JobPreparationTaskState
    :param task_root_directory: The root directory of the Job Preparation Task
     on the Compute Node. You can use this path to retrieve files created by
     the Task, such as log files.
    :type task_root_directory: str
    :param task_root_directory_url: The URL to the root directory of the Job
     Preparation Task on the Compute Node.
    :type task_root_directory_url: str
    :param exit_code: The exit code of the program specified on the Task
     command line. This parameter is returned only if the Task is in the
     completed state. The exit code for a process reflects the specific
     convention implemented by the application developer for that process. If
     you use the exit code value to make decisions in your code, be sure that
     you know the exit code convention used by the application process. Note
     that the exit code may also be generated by the Compute Node operating
     system, such as when a process is forcibly terminated.
    :type exit_code: int
    :param container_info: Information about the container under which the
     Task is executing. This property is set only if the Task runs in a
     container context.
    :type container_info:
     ~azure.batch.models.TaskContainerExecutionInformation
    :param failure_info: Information describing the Task failure, if any. This
     property is set only if the Task is in the completed state and encountered
     a failure.
    :type failure_info: ~azure.batch.models.TaskFailureInformation
    :param retry_count: Required. The number of times the Task has been
     retried by the Batch service. Task application failures (non-zero exit
     code) are retried, pre-processing errors (the Task could not be run) and
     file upload errors are not retried. The Batch service will retry the Task
     up to the limit specified by the constraints. Task application failures
     (non-zero exit code) are retried, pre-processing errors (the Task could
     not be run) and file upload errors are not retried. The Batch service will
     retry the Task up to the limit specified by the constraints.
    :type retry_count: int
    :param last_retry_time: The most recent time at which a retry of the Job
     Preparation Task started running. This property is set only if the Task
     was retried (i.e. retryCount is nonzero). If present, this is typically
     the same as startTime, but may be different if the Task has been restarted
     for reasons other than retry; for example, if the Compute Node was
     rebooted during a retry, then the startTime is updated but the
     lastRetryTime is not.
    :type last_retry_time: datetime
    :param result: The result of the Task execution. If the value is 'failed',
     then the details of the failure can be found in the failureInfo property.
     Possible values include: 'success', 'failure'
    :type result: str or ~azure.batch.models.TaskExecutionResult
    """

    _validation = {
        'start_time': {'required': True},
        'state': {'required': True},
        'retry_count': {'required': True},
    }

    _attribute_map = {
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'state': {'key': 'state', 'type': 'JobPreparationTaskState'},
        'task_root_directory': {'key': 'taskRootDirectory', 'type': 'str'},
        'task_root_directory_url': {'key': 'taskRootDirectoryUrl', 'type': 'str'},
        'exit_code': {'key': 'exitCode', 'type': 'int'},
        'container_info': {'key': 'containerInfo', 'type': 'TaskContainerExecutionInformation'},
        'failure_info': {'key': 'failureInfo', 'type': 'TaskFailureInformation'},
        'retry_count': {'key': 'retryCount', 'type': 'int'},
        'last_retry_time': {'key': 'lastRetryTime', 'type': 'iso-8601'},
        'result': {'key': 'result', 'type': 'TaskExecutionResult'},
    }

    def __init__(self, *, start_time, state, retry_count: int, end_time=None, task_root_directory: str=None, task_root_directory_url: str=None, exit_code: int=None, container_info=None, failure_info=None, last_retry_time=None, result=None, **kwargs) -> None:
        super(JobPreparationTaskExecutionInformation, self).__init__(**kwargs)
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
        self.task_root_directory = task_root_directory
        self.task_root_directory_url = task_root_directory_url
        self.exit_code = exit_code
        self.container_info = container_info
        self.failure_info = failure_info
        self.retry_count = retry_count
        self.last_retry_time = last_retry_time
        self.result = result
