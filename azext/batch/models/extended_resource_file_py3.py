# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.batch.models import ResourceFile


class ExtendedResourceFile(ResourceFile):
    """A file to be downloaded from Azure blob storage to a compute node.

    :param http_url: The URL of the file within Azure Blob Storage. This
     URL must be readable using anonymous access; that is, the Batch service
     does not present any credentials when downloading the blob. There are two
     ways to get such a URL for a blob in Azure storage: include a Shared
     Access Signature (SAS) granting read permissions on the blob, or set the
     ACL for the blob or its container to allow public access.
    :type http_url: str
    :param auto_storage_container_name: The storage container name in the auto
    storage account. The autoStorageContainerName, storageContainerUrl and
    httpUrl properties are mutually exclusive and one of them must be specified.
    :type auto_storage_container_name: str
    :param storage_container_url: The URL of the blob container within Azure
    Blob Storage. The autoStorageContainerName, storageContainerUrl and httpUrl
    properties are mutually exclusive and one of them must be specified. This
    URL must be readable and listable using anonymous access; that is, the
    Batch service does not present any credentials when downloading blobs from
    the container. There are two ways to get such a URL for a container in
    Azure storage: include a Shared Access Signature (SAS) granting read and
    list permissions on the container, or set the ACL for the container to
    allow public access.
    :type storage_container_url: str
    :param blob_prefix: The blob prefix to use when downloading blobs from an
    Azure Storage container. Only the blobs whose names begin with the specified
    prefix will be downloaded. The property is valid only when
    autoStorageContainerName or storageContainerUrl is used. This prefix can be
    a partial filename or a subdirectory. If a prefix is not specified, all the
    files in the container will be downloaded.
    :type blob_prefix: str
    :param file_path: The location on the compute node to which to download
     the file, relative to the task's working directory. If using a file group
     source that references more than one file, this will be considered the name
     of a directory, otherwise it will be treated as the destination file name.
    :type file_path: str
    :param file_mode: The file permission mode attribute in octal format. This
     property applies only to files being downloaded to Linux compute nodes. It
     will be ignored if it is specified for a resourceFile which will be
     downloaded to a Windows node. If this property is not specified for a
     Linux node, then a default value of 0770 is applied to the file.
     If using a file group source that references more than one file, this will be
     applied to all files in the group.
    :type file_mode: str
    :param source: A file source reference which could include a collection of files from
     a Azure Storage container or an auto-storage file group.
    :type source: :class:`FileSource
     <azext.batch.models.FileSource>`
    """

    _attribute_map = {
        'http_url': {'key': 'httpUrl', 'type': 'str'},
        'auto_storage_container_name': {'key': 'autoStorageContainerName', 'type': 'str'},
        'blob_prefix': {'key': 'blobPrefix', 'type': 'str'},
        'storage_container_url': {'key': 'storageContainerUrl', 'type': 'str'},
        'file_path': {'key': 'filePath', 'type': 'str'},
        'file_mode': {'key': 'fileMode', 'type': 'str'},
        'source': {'key': 'source', 'type': 'FileSource'}
    }

    def __init__(self,
                 *,
                 http_url: str=None,
                 auto_storage_container_name: str=None,
                 storage_container_url: str=None,
                 blob_prefix: str=None,
                 file_path: str=None,
                 file_mode: str=None,
                 source=None, **kwargs) -> None:
        super(ExtendedResourceFile, self).__init__(
            http_url=http_url,
            auto_storage_container_name=auto_storage_container_name,
            storage_container_url=storage_container_url,
            blob_prefix=blob_prefix,
            file_path=file_path,
            file_mode=file_mode,
            **kwargs)
        self.source = source
