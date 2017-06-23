# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class JobTemplate(Model):

    _validation = {
        'type': {'required': True, 'constant': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'id', 'type': 'str'},
        'api_version': {'key': 'apiVersion', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'ExtendedJobParameter'},
    }

    type = "Microsoft.Batch/batchAccounts/jobs"

    def __init__(self, properties, api_version=None):
        self.properties = properties
        self.api_version = api_version
