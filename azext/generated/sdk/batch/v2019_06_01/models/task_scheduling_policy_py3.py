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


class TaskSchedulingPolicy(Model):
    """Specifies how Tasks should be distributed across Compute Nodes.

    All required parameters must be populated in order to send to Azure.

    :param node_fill_type: Required. How Tasks are distributed across Compute
     Nodes in a Pool. If not specified, the default is spread. Possible values
     include: 'spread', 'pack'
    :type node_fill_type: str or ~azure.batch.models.ComputeNodeFillType
    """

    _validation = {
        'node_fill_type': {'required': True},
    }

    _attribute_map = {
        'node_fill_type': {'key': 'nodeFillType', 'type': 'ComputeNodeFillType'},
    }

    def __init__(self, *, node_fill_type, **kwargs) -> None:
        super(TaskSchedulingPolicy, self).__init__(**kwargs)
        self.node_fill_type = node_fill_type
