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


class TaskInformation(Model):
    """Information about a Task running on a Compute Node.

    All required parameters must be populated in order to send to Azure.

    :param task_url: The URL of the Task.
    :type task_url: str
    :param job_id: The ID of the Job to which the Task belongs.
    :type job_id: str
    :param task_id: The ID of the Task.
    :type task_id: str
    :param subtask_id: The ID of the subtask if the Task is a multi-instance
     Task.
    :type subtask_id: int
    :param task_state: Required. The current state of the Task. Possible
     values include: 'active', 'preparing', 'running', 'completed'
    :type task_state: str or ~azure.batch.models.TaskState
    :param execution_info: Information about the execution of the Task.
    :type execution_info: ~azure.batch.models.TaskExecutionInformation
    """

    _validation = {
        'task_state': {'required': True},
    }

    _attribute_map = {
        'task_url': {'key': 'taskUrl', 'type': 'str'},
        'job_id': {'key': 'jobId', 'type': 'str'},
        'task_id': {'key': 'taskId', 'type': 'str'},
        'subtask_id': {'key': 'subtaskId', 'type': 'int'},
        'task_state': {'key': 'taskState', 'type': 'TaskState'},
        'execution_info': {'key': 'executionInfo', 'type': 'TaskExecutionInformation'},
    }

    def __init__(self, **kwargs):
        super(TaskInformation, self).__init__(**kwargs)
        self.task_url = kwargs.get('task_url', None)
        self.job_id = kwargs.get('job_id', None)
        self.task_id = kwargs.get('task_id', None)
        self.subtask_id = kwargs.get('subtask_id', None)
        self.task_state = kwargs.get('task_state', None)
        self.execution_info = kwargs.get('execution_info', None)
