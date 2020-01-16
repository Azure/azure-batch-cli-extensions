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


class JobPreparationAndReleaseTaskExecutionInformation(Model):
    """The status of the Job Preparation and Job Release Tasks on a Compute Node.

    :param pool_id: The ID of the Pool containing the Compute Node to which
     this entry refers.
    :type pool_id: str
    :param node_id: The ID of the Compute Node to which this entry refers.
    :type node_id: str
    :param node_url: The URL of the Compute Node to which this entry refers.
    :type node_url: str
    :param job_preparation_task_execution_info: Information about the
     execution status of the Job Preparation Task on this Compute Node.
    :type job_preparation_task_execution_info:
     ~azure.batch.models.JobPreparationTaskExecutionInformation
    :param job_release_task_execution_info: Information about the execution
     status of the Job Release Task on this Compute Node. This property is set
     only if the Job Release Task has run on the Compute Node.
    :type job_release_task_execution_info:
     ~azure.batch.models.JobReleaseTaskExecutionInformation
    """

    _attribute_map = {
        'pool_id': {'key': 'poolId', 'type': 'str'},
        'node_id': {'key': 'nodeId', 'type': 'str'},
        'node_url': {'key': 'nodeUrl', 'type': 'str'},
        'job_preparation_task_execution_info': {'key': 'jobPreparationTaskExecutionInfo', 'type': 'JobPreparationTaskExecutionInformation'},
        'job_release_task_execution_info': {'key': 'jobReleaseTaskExecutionInfo', 'type': 'JobReleaseTaskExecutionInformation'},
    }

    def __init__(self, **kwargs):
        super(JobPreparationAndReleaseTaskExecutionInformation, self).__init__(**kwargs)
        self.pool_id = kwargs.get('pool_id', None)
        self.node_id = kwargs.get('node_id', None)
        self.node_url = kwargs.get('node_url', None)
        self.job_preparation_task_execution_info = kwargs.get('job_preparation_task_execution_info', None)
        self.job_release_task_execution_info = kwargs.get('job_release_task_execution_info', None)
