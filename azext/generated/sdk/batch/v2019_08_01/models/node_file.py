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


class NodeFile(Model):
    """Information about a file or directory on a Compute Node.

    :param name: The file path.
    :type name: str
    :param url: The URL of the file.
    :type url: str
    :param is_directory: Whether the object represents a directory.
    :type is_directory: bool
    :param properties: The file properties.
    :type properties: ~azure.batch.models.FileProperties
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'url': {'key': 'url', 'type': 'str'},
        'is_directory': {'key': 'isDirectory', 'type': 'bool'},
        'properties': {'key': 'properties', 'type': 'FileProperties'},
    }

    def __init__(self, **kwargs):
        super(NodeFile, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.url = kwargs.get('url', None)
        self.is_directory = kwargs.get('is_directory', None)
        self.properties = kwargs.get('properties', None)
