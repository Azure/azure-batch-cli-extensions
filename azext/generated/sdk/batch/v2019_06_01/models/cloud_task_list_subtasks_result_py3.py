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


class CloudTaskListSubtasksResult(Model):
    """The result of listing the subtasks of a Task.

    :param value: The list of subtasks.
    :type value: list[~azure.batch.models.SubtaskInformation]
    """

    _attribute_map = {
        'value': {'key': 'value', 'type': '[SubtaskInformation]'},
    }

    def __init__(self, *, value=None, **kwargs) -> None:
        super(CloudTaskListSubtasksResult, self).__init__(**kwargs)
        self.value = value
