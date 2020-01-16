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


class JobExecutionInformation(Model):
    """Contains information about the execution of a Job in the Azure Batch
    service.

    All required parameters must be populated in order to send to Azure.

    :param start_time: Required. The start time of the Job. This is the time
     at which the Job was created.
    :type start_time: datetime
    :param end_time: The completion time of the Job. This property is set only
     if the Job is in the completed state.
    :type end_time: datetime
    :param pool_id: The ID of the Pool to which this Job is assigned. This
     element contains the actual Pool where the Job is assigned. When you get
     Job details from the service, they also contain a poolInfo element, which
     contains the Pool configuration data from when the Job was added or
     updated. That poolInfo element may also contain a poolId element. If it
     does, the two IDs are the same. If it does not, it means the Job ran on an
     auto Pool, and this property contains the ID of that auto Pool.
    :type pool_id: str
    :param scheduling_error: Details of any error encountered by the service
     in starting the Job. This property is not set if there was no error
     starting the Job.
    :type scheduling_error: ~azure.batch.models.JobSchedulingError
    :param terminate_reason: A string describing the reason the Job ended.
     This property is set only if the Job is in the completed state. If the
     Batch service terminates the Job, it sets the reason as follows:
     JMComplete - the Job Manager Task completed, and killJobOnCompletion was
     set to true. MaxWallClockTimeExpiry - the Job reached its maxWallClockTime
     constraint. TerminateJobSchedule - the Job ran as part of a schedule, and
     the schedule terminated. AllTasksComplete - the Job's onAllTasksComplete
     attribute is set to terminatejob, and all Tasks in the Job are complete.
     TaskFailed - the Job's onTaskFailure attribute is set to
     performExitOptionsJobAction, and a Task in the Job failed with an exit
     condition that specified a jobAction of terminatejob. Any other string is
     a user-defined reason specified in a call to the 'Terminate a Job'
     operation.
    :type terminate_reason: str
    """

    _validation = {
        'start_time': {'required': True},
    }

    _attribute_map = {
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'pool_id': {'key': 'poolId', 'type': 'str'},
        'scheduling_error': {'key': 'schedulingError', 'type': 'JobSchedulingError'},
        'terminate_reason': {'key': 'terminateReason', 'type': 'str'},
    }

    def __init__(self, *, start_time, end_time=None, pool_id: str=None, scheduling_error=None, terminate_reason: str=None, **kwargs) -> None:
        super(JobExecutionInformation, self).__init__(**kwargs)
        self.start_time = start_time
        self.end_time = end_time
        self.pool_id = pool_id
        self.scheduling_error = scheduling_error
        self.terminate_reason = terminate_reason
