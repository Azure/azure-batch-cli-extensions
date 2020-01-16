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


class NFSMountConfiguration(Model):
    """Information used to connect to an NFS file system.

    All required parameters must be populated in order to send to Azure.

    :param source: Required. The URI of the file system to mount.
    :type source: str
    :param relative_mount_path: Required. The relative path on the compute
     node where the file system will be mounted. All file systems are mounted
     relative to the Batch mounts directory, accessible via the
     AZ_BATCH_NODE_MOUNTS_DIR environment variable.
    :type relative_mount_path: str
    :param mount_options: Additional command line options to pass to the mount
     command. These are 'net use' options in Windows and 'mount' options in
     Linux.
    :type mount_options: str
    """

    _validation = {
        'source': {'required': True},
        'relative_mount_path': {'required': True},
    }

    _attribute_map = {
        'source': {'key': 'source', 'type': 'str'},
        'relative_mount_path': {'key': 'relativeMountPath', 'type': 'str'},
        'mount_options': {'key': 'mountOptions', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(NFSMountConfiguration, self).__init__(**kwargs)
        self.source = kwargs.get('source', None)
        self.relative_mount_path = kwargs.get('relative_mount_path', None)
        self.mount_options = kwargs.get('mount_options', None)
