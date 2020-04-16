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


class UploadBatchServiceLogsResult(Model):
    """The result of uploading Batch service log files from a specific Compute
    Node.

    All required parameters must be populated in order to send to Azure.

    :param virtual_directory_name: Required. The virtual directory within
     Azure Blob Storage container to which the Batch Service log file(s) will
     be uploaded. The virtual directory name is part of the blob name for each
     log file uploaded, and it is built based poolId, nodeId and a unique
     identifier.
    :type virtual_directory_name: str
    :param number_of_files_uploaded: Required. The number of log files which
     will be uploaded.
    :type number_of_files_uploaded: int
    """

    _validation = {
        'virtual_directory_name': {'required': True},
        'number_of_files_uploaded': {'required': True},
    }

    _attribute_map = {
        'virtual_directory_name': {'key': 'virtualDirectoryName', 'type': 'str'},
        'number_of_files_uploaded': {'key': 'numberOfFilesUploaded', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(UploadBatchServiceLogsResult, self).__init__(**kwargs)
        self.virtual_directory_name = kwargs.get('virtual_directory_name', None)
        self.number_of_files_uploaded = kwargs.get('number_of_files_uploaded', None)
