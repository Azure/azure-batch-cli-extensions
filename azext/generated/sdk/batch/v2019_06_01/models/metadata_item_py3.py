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


class MetadataItem(Model):
    """A name-value pair associated with a Batch service resource.

    The Batch service does not assign any meaning to this metadata; it is
    solely for the use of user code.

    All required parameters must be populated in order to send to Azure.

    :param name: Required. The name of the metadata item.
    :type name: str
    :param value: Required. The value of the metadata item.
    :type value: str
    """

    _validation = {
        'name': {'required': True},
        'value': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
    }

    def __init__(self, *, name: str, value: str, **kwargs) -> None:
        super(MetadataItem, self).__init__(**kwargs)
        self.name = name
        self.value = value
