# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import unicode_literals

import errno
import os

from azure.batch.operations.file_operations import FileOperations
from azure.storage.blob.models import Include

from .. import _file_utils as file_utils


class ExtendedFileOperations(FileOperations):
    """FileOperations operations.

    :param parent: The parent BatchExtensionsClient object.
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :param get_storage_account: A callable to retrieve a storage client object.
    """
    def __init__(self, parent, client, config, serializer, deserializer, get_storage_account):
        super(ExtendedFileOperations, self).__init__(client, config, serializer, deserializer)
        self._parent = parent
        self.get_storage_client = get_storage_account

    def generate_sas_url(self, file_group, file_name, remote_path=None):
        """Generate a SAS URL for a specific file in an exiting file group.
        :param str file_group: The file group into the file was uploaded.
        :param str file_name: The name of the file to generate the URL for.
        :param str remote_path: The subfoder in the file group under which the file
         was uploaded.
        :returns: The URL (str).
        """
        container = file_utils.get_container_name(file_group)
        storage_client = self.get_storage_client()
        if remote_path:
            # Add any specified virtual directories
            blob_prefix = remote_path.strip('\\/')
            file_name = '{}/{}'.format(blob_prefix, file_name.strip('\\/'))
        try:
            blob = storage_client.get_blob_properties(container, file_name)
        except Exception as exp:  # TODO: Catch specific error.
            raise ValueError("Unable to locate blob '{}' in container '{}'. Error: {}".format(
                file_name, container, exp))
        else:
            return file_utils.generate_blob_sas_token(blob, container, storage_client)

    def upload(self, local_path, file_group, remote_path=None, flatten=None, progress_callback=None):
        """Upload local file or directory of files to storage
        :param str local_path: The full path to the local file or directory or files.
         Also supports * and ** notation.
        :param str file_group: The name of the file group under which to upload the files.
        :param str remote_path: A subfolder path to upload the files to.
        :param bool flatten: Whether to flatten the local directory structure when uploading.
         The default is False, where the local directory strucutre will be maintained.
        :param func progress_callback: A callback function to monitor progress of an individual
         file upload. Must take two parameters, the data uploaded so far (int) and the total
         data to be uploaded (int), both in bytes.
        """
        path, files = file_utils.resolve_file_paths(local_path)
        if len(files) > 0:
            for f in files:  # TODO: Threaded pool.
                file_name = os.path.relpath(f, path)
                file_utils.upload_blob(f, file_group, file_name, self.get_storage_client(),
                                       remote_path=remote_path, flatten=flatten,
                                       progress_callback=progress_callback)
        else:
            raise ValueError('No files or directories found matching local path {}'.format(local_path))

    def download(self, local_path, file_group, remote_path=None,
                 overwrite=False, progress_callback=None):
        """Download the contents of a file group, optionally relative to a subfolder.
        :param str local_path: The directory into which the files will be downloaded. If
         the files have a remote folder structure, this will be maintained relative to this
         directory.
        :param str file_group: The file group from which to download files.
        :param str remote_path: The subfolder from which to download files or file name prefix.
        :param bool overwrite: Whether to overwrite files if the already exist at the local
         path specified.
        :param func progress_callback: A function to monitor progress of the download of an
         individual file. Must take two parameters, the data so far retrieved (int) and the
         total data to be retrieved (int) both in bytes.
        """
        storage_client = self.get_storage_client()
        files = file_utils.resolve_remote_paths(storage_client, file_group, remote_path)
        if files:
            for f in files:
                file_name = os.path.realpath(os.path.join(local_path, f.name))
                if not os.path.exists(file_name) or overwrite:
                    if not os.path.exists(os.path.dirname(file_name)):
                        try:
                            os.makedirs(os.path.dirname(file_name))
                        except OSError as exc: # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    file_utils.download_blob(f.name, file_group, file_name,
                                             storage_client, progress_callback)
        else:
            raise ValueError('No files found in file group {} matching remote path {}'.format(
                file_group, remote_path))

    def list_groups(self, num_results=None):
        """List the file group names in the storage account.
        :param int num_results: The max number of file group names to return.
        :returns: A generator of file groups. Each file group is represented as a dictionary with
         the following keys:
         'name': The file group name.
         'last_modified': The time stamp for when the file group was created (or last modified).
        """
        storage_client = self.get_storage_client()
        prefix = file_utils.FileUtils.GROUP_PREFIX
        return ({'name': c.name[len(prefix):], 'last_modified': c.properties.last_modified}
                for c in storage_client.list_containers(prefix=prefix, num_results=num_results))

    def list_from_group(self, file_group, remote_path=None, num_results=None):
        """List the files in the file group.
        :param str file_group: The file group from which to list the files.
        :param str remote_path: The remote file prefix by which to filter results.
        :param int num_results: The max number of files to return.
        :returns: A generator of files. Each file is represented as a dictionary with
         the following keys:
         'name': The full remote file path.
         'last_modified': The time stamp for when the file was last modified locally.
         'size': The content length of the file.
         'uploaded': The time stamp for whe the file was last modified remotely.
        """
        storage_client = self.get_storage_client()
        container = file_utils.get_container_name(file_group)
        properties = Include(metadata=True)
        return ({'name': b.name,
                 'last_modified': b.metadata.get('lastmodified'),
                 'size': b.properties.content_length,
                 'uploaded': b.properties.last_modified}
                for b in storage_client.list_blobs(
                    container, prefix=remote_path, num_results=num_results, include=properties))

    def delete_group(self, file_group):
        """Attempt to delete the file group and all of it's contents.
        Will do nothing if the group does not exist.
        :param str file_group: The file group to delete.
        :returns: True if file group deleted, otherwise False.
        """
        storage_client = self.get_storage_client()
        container = file_utils.get_container_name(file_group)
        return storage_client.delete_container(container, fail_not_exist=False)
