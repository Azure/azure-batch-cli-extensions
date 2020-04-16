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


class TaskIdRange(Model):
    """A range of Task IDs that a Task can depend on. All Tasks with IDs in the
    range must complete successfully before the dependent Task can be
    scheduled.

    The start and end of the range are inclusive. For example, if a range has
    start 9 and end 12, then it represents Tasks '9', '10', '11' and '12'.

    All required parameters must be populated in order to send to Azure.

    :param start: Required. The first Task ID in the range.
    :type start: int
    :param end: Required. The last Task ID in the range.
    :type end: int
    """

    _validation = {
        'start': {'required': True},
        'end': {'required': True},
    }

    _attribute_map = {
        'start': {'key': 'start', 'type': 'int'},
        'end': {'key': 'end', 'type': 'int'},
    }

    def __init__(self, *, start: int, end: int, **kwargs) -> None:
        super(TaskIdRange, self).__init__(**kwargs)
        self.start = start
        self.end = end
