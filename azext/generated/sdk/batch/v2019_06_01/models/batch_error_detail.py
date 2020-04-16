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


class BatchErrorDetail(Model):
    """An item of additional information included in an Azure Batch error
    response.

    :param key: An identifier specifying the meaning of the Value property.
    :type key: str
    :param value: The additional information included with the error response.
    :type value: str
    """

    _attribute_map = {
        'key': {'key': 'key', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(BatchErrorDetail, self).__init__(**kwargs)
        self.key = kwargs.get('key', None)
        self.value = kwargs.get('value', None)
