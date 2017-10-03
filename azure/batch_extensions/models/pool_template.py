# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.serialization import Model


class PoolTemplate(Model):
    """A Pool Template.

    :ivar type: The type of object described by the template. Must be:
     "Microsoft.Batch/batchAccounts/pools"
    :type type: str
    :param api_version: The API version that the template conforms to.
    :type api_version: str
    :param properties: The specificaton of the pool.
    :type properties: :class:`ExtendedPoolParameter<azure.batch_extensions.models.ExtendedPoolParameter>`
    """

    _validation = {
        'type': {'required': True, 'constant': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'id', 'type': 'str'},
        'api_version': {'key': 'apiVersion', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'ExtendedPoolParameter'},
    }

    type = "Microsoft.Batch/batchAccounts/pools"

    def __init__(self, properties, api_version=None):
        self.properties = properties
        self.api_version = api_version
