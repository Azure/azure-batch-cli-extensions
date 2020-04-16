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


class StartTaskInformation(Model):
    """Information about a start Task running on a Compute Node.

    All required parameters must be populated in order to send to Azure.

    :param state: Required. The state of the start Task on the Compute Node.
     Possible values include: 'running', 'completed'
    :type state: str or ~azure.batch.models.StartTaskState
    :param start_time: Required. The time at which the start Task started
     running. This value is reset every time the Task is restarted or retried
     (that is, this is the most recent time at which the start Task started
     running).
    :type start_time: datetime
    :param end_time: The time at which the start Task stopped running. This is
     the end time of the most recent run of the start Task, if that run has
     completed (even if that run failed and a retry is pending). This element
     is not present if the start Task is currently running.
    :type end_time: datetime
    :param exit_code: The exit code of the program specified on the start Task
     command line. This property is set only if the start Task is in the
     completed state. In general, the exit code for a process reflects the
     specific convention implemented by the application developer for that
     process. If you use the exit code value to make decisions in your code, be
     sure that you know the exit code convention used by the application
     process. However, if the Batch service terminates the start Task (due to
     timeout, or user termination via the API) you may see an operating
     system-defined exit code.
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
     up to the limit specified by the constraints.
    :type retry_count: int
    :param last_retry_time: The most recent time at which a retry of the Task
     started running. This element is present only if the Task was retried
     (i.e. retryCount is nonzero). If present, this is typically the same as
     startTime, but may be different if the Task has been restarted for reasons
     other than retry; for example, if the Compute Node was rebooted during a
     retry, then the startTime is updated but the lastRetryTime is not.
    :type last_retry_time: datetime
    :param result: The result of the Task execution. If the value is 'failed',
     then the details of the failure can be found in the failureInfo property.
     Possible values include: 'success', 'failure'
    :type result: str or ~azure.batch.models.TaskExecutionResult
    """

    _validation = {
        'state': {'required': True},
        'start_time': {'required': True},
        'retry_count': {'required': True},
    }

    _attribute_map = {
        'state': {'key': 'state', 'type': 'StartTaskState'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'exit_code': {'key': 'exitCode', 'type': 'int'},
        'container_info': {'key': 'containerInfo', 'type': 'TaskContainerExecutionInformation'},
        'failure_info': {'key': 'failureInfo', 'type': 'TaskFailureInformation'},
        'retry_count': {'key': 'retryCount', 'type': 'int'},
        'last_retry_time': {'key': 'lastRetryTime', 'type': 'iso-8601'},
        'result': {'key': 'result', 'type': 'TaskExecutionResult'},
    }

    def __init__(self, *, state, start_time, retry_count: int, end_time=None, exit_code: int=None, container_info=None, failure_info=None, last_retry_time=None, result=None, **kwargs) -> None:
        super(StartTaskInformation, self).__init__(**kwargs)
        self.state = state
        self.start_time = start_time
        self.end_time = end_time
        self.exit_code = exit_code
        self.container_info = container_info
        self.failure_info = failure_info
        self.retry_count = retry_count
        self.last_retry_time = last_retry_time
        self.result = result
