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


class FileProperties(Model):
    """The properties of a file on a Compute Node.

    All required parameters must be populated in order to send to Azure.

    :param creation_time: The file creation time. The creation time is not
     returned for files on Linux Compute Nodes.
    :type creation_time: datetime
    :param last_modified: Required. The time at which the file was last
     modified.
    :type last_modified: datetime
    :param content_length: Required. The length of the file.
    :type content_length: long
    :param content_type: The content type of the file.
    :type content_type: str
    :param file_mode: The file mode attribute in octal format. The file mode
     is returned only for files on Linux Compute Nodes.
    :type file_mode: str
    """

    _validation = {
        'last_modified': {'required': True},
        'content_length': {'required': True},
    }

    _attribute_map = {
        'creation_time': {'key': 'creationTime', 'type': 'iso-8601'},
        'last_modified': {'key': 'lastModified', 'type': 'iso-8601'},
        'content_length': {'key': 'contentLength', 'type': 'long'},
        'content_type': {'key': 'contentType', 'type': 'str'},
        'file_mode': {'key': 'fileMode', 'type': 'str'},
    }

    def __init__(self, *, last_modified, content_length: int, creation_time=None, content_type: str=None, file_mode: str=None, **kwargs) -> None:
        super(FileProperties, self).__init__(**kwargs)
        self.creation_time = creation_time
        self.last_modified = last_modified
        self.content_length = content_length
        self.content_type = content_type
        self.file_mode = file_mode
