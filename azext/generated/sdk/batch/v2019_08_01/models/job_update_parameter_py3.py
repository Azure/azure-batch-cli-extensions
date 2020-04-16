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


class JobUpdateParameter(Model):
    """The set of changes to be made to a Job.

    All required parameters must be populated in order to send to Azure.

    :param priority: The priority of the Job. Priority values can range from
     -1000 to 1000, with -1000 being the lowest priority and 1000 being the
     highest priority. If omitted, it is set to the default value 0.
    :type priority: int
    :param constraints: The execution constraints for the Job. If omitted, the
     constraints are cleared.
    :type constraints: ~azure.batch.models.JobConstraints
    :param pool_info: Required. The Pool on which the Batch service runs the
     Job's Tasks. You may change the Pool for a Job only when the Job is
     disabled. The Update Job call will fail if you include the poolInfo
     element and the Job is not disabled. If you specify an
     autoPoolSpecification in the poolInfo, only the keepAlive property of the
     autoPoolSpecification can be updated, and then only if the
     autoPoolSpecification has a poolLifetimeOption of Job (other job
     properties can be updated as normal).
    :type pool_info: ~azure.batch.models.PoolInformation
    :param metadata: A list of name-value pairs associated with the Job as
     metadata. If omitted, it takes the default value of an empty list; in
     effect, any existing metadata is deleted.
    :type metadata: list[~azure.batch.models.MetadataItem]
    :param on_all_tasks_complete: The action the Batch service should take
     when all Tasks in the Job are in the completed state. If omitted, the
     completion behavior is set to noaction. If the current value is
     terminatejob, this is an error because a Job's completion behavior may not
     be changed from terminatejob to noaction. You may not change the value
     from terminatejob to noaction - that is, once you have engaged automatic
     Job termination, you cannot turn it off again. If you try to do this, the
     request fails and Batch returns status code 400 (Bad Request) and an
     'invalid property value' error response. If you do not specify this
     element in a PUT request, it is equivalent to passing noaction. This is an
     error if the current value is terminatejob. Possible values include:
     'noAction', 'terminateJob'
    :type on_all_tasks_complete: str or ~azure.batch.models.OnAllTasksComplete
    """

    _validation = {
        'pool_info': {'required': True},
    }

    _attribute_map = {
        'priority': {'key': 'priority', 'type': 'int'},
        'constraints': {'key': 'constraints', 'type': 'JobConstraints'},
        'pool_info': {'key': 'poolInfo', 'type': 'PoolInformation'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
        'on_all_tasks_complete': {'key': 'onAllTasksComplete', 'type': 'OnAllTasksComplete'},
    }

    def __init__(self, *, pool_info, priority: int=None, constraints=None, metadata=None, on_all_tasks_complete=None, **kwargs) -> None:
        super(JobUpdateParameter, self).__init__(**kwargs)
        self.priority = priority
        self.constraints = constraints
        self.pool_info = pool_info
        self.metadata = metadata
        self.on_all_tasks_complete = on_all_tasks_complete
