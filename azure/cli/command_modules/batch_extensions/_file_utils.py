# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import re
import hashlib
import datetime
import copy
import pathlib
from six.moves.urllib.parse import urlsplit  # pylint: disable=import-error
from six.moves.urllib.parse import quote  # pylint: disable=import-error

from msrestazure.azure_exceptions import CloudError
from azure.mgmt.storage import StorageManagementClient
from azure.storage import CloudStorageAccount
from azure.storage.blob import BlobPermissions, BlockBlobService
from azure.mgmt.batch import BatchManagementClient

from azure.cli.core.commands.client_factory import get_mgmt_service_client
import azure.cli.core.azlogging as azlogging
from azure.cli.core._config import az_config

logger = azlogging.get_az_logger(__name__)


def construct_sas_url(blob, uri):
    """Make up blob URL with container URL"""
    newuri = copy.copy(uri)
    newuri.pathname = '{}/{}'.format(uri.path, quote(blob.name))
    return newuri.geturl()


def convert_blobs_to_resource_files(blobs, resource_properties):
    """Convert a list of blobs to a list of ResourceFiles"""
    resource_files = []
    if not blobs:
        raise ValueError('No input data found with reference {}'.
                         format(resource_properties['source']['prefix']))

    prefix = resource_properties.get('source', {}).get('prefix')
    if len(blobs) == 1 and blobs[0]['filePath'] == prefix:
        # Single file reference: filePath should be treated as file path
        file_path = resource_properties.get('filePath', blobs[0]['filePath'])
        resource_files.append({
            'blobSource': blobs[0]['url'],
            'filePath': file_path
        })
    else:
        # Multiple file reference: filePath should be treated as a directory
        base_file_path = ''
        if 'filePath' in resource_properties:
            base_file_path = '{}/'.format(
                FileUtils.STRIP_PATH.sub('', resource_properties['filePath']))

        for blob in blobs:
            file_path = '{}{}'.format(base_file_path, blob['filePath'])
            resource_files.append({
                'blobSource': blob['url'],
                'filePath': file_path
            })

    # Add filemode to every resourceFile
    if 'fileMode' in resource_properties:
        for f in resource_files:
            f['fileMode'] = resource_properties['fileMode']

    return resource_files


def resolve_file_paths(local_path):
    """Generate list of files to upload and the relative directory"""
    local_path = FileUtils.STRIP_PATH.sub("", local_path)
    files = []
    if local_path.find('*') > -1:
        # Supplied path is a pattern - relative directory will be the
        # path up to the first wildcard
        ref_dir_str = local_path.split('*')[0]
        ref_dir_str = FileUtils.STRIP_PATH.sub("", ref_dir_str)
        if not os.path.isdir(ref_dir_str):
            ref_dir_str = os.path.dirname(ref_dir_str)
        ref_dir = pathlib.Path(ref_dir_str)
        pattern = local_path[len(ref_dir_str + os.pathsep):]
        files = [str(f) for f in ref_dir.glob(pattern) if f.is_file()]
        local_path = ref_dir_str
    else:
        if os.path.isdir(local_path):
            # Supplied path is a directory
            files = [os.path.join(local_path, f) for f in os.listdir(local_path)
                     if os.path.isfile(os.path.join(local_path, f))]
        elif os.path.isfile(local_path):
            # Supplied path is a file
            files.append(local_path)
            local_path = os.path.dirname(local_path)
    return local_path, files


def resolve_remote_paths(blob_service, file_group, remote_path):
    blobs = blob_service.list_blobs(_get_container_name(file_group), prefix=remote_path)
    return list(blobs)

def generate_container_name(file_group):
    """Generate valid container name from file group name."""
    file_group = file_group.lower()
    # Check for any chars that aren't 'a-z', '0-9' or '-'
    valid_chars = r'^[a-z0-9][-a-z0-9]*$'
    # Replace any underscores or double-hyphens with single hyphen
    underscores_and_hyphens = r'[_-]+'

    clean_group = re.sub(underscores_and_hyphens, '-', file_group)
    clean_group = clean_group.rstrip('-')
    if not re.match(valid_chars, clean_group):
        raise ValueError('File group name \'{}\' contains illegal characters. '
                         'File group names only support alphanumeric characters, '
                         'underscores and hyphens.'.format(file_group))

    if clean_group == file_group and len(file_group) <= FileUtils.MAX_GROUP_LENGTH:
        # If specified group name is clean, no need to add hash
        return file_group
    else:
        # If we had to transform the group name, add hash of original name
        hash_str = hashlib.sha1(file_group.encode()).hexdigest()
        new_group = '{}-{}'.format(clean_group, hash_str)
        if len(new_group) > FileUtils.MAX_GROUP_LENGTH:
            return '{}-{}'.format(clean_group[0:15], hash_str)
        return new_group


def _get_container_name(file_group):
    """Get valid container name from file group name with prefix."""
    return '{}{}'.format(FileUtils.GROUP_PREFIX, generate_container_name(file_group))


def _generate_blob_sas_token(blob, container, blob_service, permission=BlobPermissions.READ):
    """Generate a blob URL with SAS token."""
    sas_token = blob_service.generate_blob_shared_access_signature(
        container, blob.name,
        permission=permission,
        start=datetime.datetime.utcnow(),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(days=FileUtils.SAS_EXPIRY_DAYS))
    return blob_service.make_blob_url(container, quote(blob.name), sas_token=sas_token)


def _generate_container_sas_token(container, blob_service, permission=BlobPermissions.WRITE):
    """Generate a container URL with SAS token."""
    blob_service.create_container(container)
    sas_token = blob_service.generate_container_shared_access_signature(
        container,
        permission=permission,
        start=datetime.datetime.utcnow(),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(days=FileUtils.SAS_EXPIRY_DAYS))
    url = '{}://{}/{}?{}'.format(
        blob_service.protocol,
        blob_service.primary_endpoint,
        container,
        sas_token)
    return url

def download_blob(blob, file_group, destination, blob_service):
    """Download the specified file to the specified container"""
    blob_service.get_blob_to_path(_get_container_name(file_group), blob, destination)

def upload_blob(source, destination, file_name,  # pylint: disable=too-many-arguments
                blob_service, remote_path=None, flatten=None):
    """Upload the specified file to the specified container"""
    if not os.path.isfile(source):
        raise ValueError('Failed to locate file {}'.format(source))

    statinfo = os.stat(source)
    if statinfo.st_size > 50000 * 4 * 1024 * 1024:
        raise ValueError('The local file size {} exceeds the Azure blob size limit'.
                         format(statinfo.st_size))
    if flatten:
        # Flatten local directory structure
        file_name = os.path.basename(file_name)

    # Create upload container with sanitized file group name
    container_name = _get_container_name(destination)
    blob_service.create_container(container_name)

    blob_name = file_name
    if remote_path:
        # Add any specified virtual directories
        blob_prefix = FileUtils.STRIP_PATH.sub('', remote_path)
        blob_name = '{}/{}'.format(blob_prefix, FileUtils.STRIP_PATH.sub('', file_name))
    blob_name = blob_name.replace('\\', '/')

    # We store the lastmodified timestamp in order to prevent overwriting with
    # out-dated or duplicate data. TODO: Investigate cleaner options for handling this.
    file_time = str(os.path.getmtime(source))
    metadata = None
    try:
        metadata = blob_service.get_blob_metadata(container_name, blob_name)
    except Exception:  # pylint: disable=broad-except
        # check notfound
        pass
    else:
        if metadata and metadata['lastmodified']:
            if metadata['lastmodified'] == file_time:
                logger.warning('File \'%s\' already exists and up-to-date - skipping', blob_name)
                return

    logger.warning('Uploading %s to blob %s in container %s', source, blob_name, container_name)
    # Upload block blob
    # TODO: Investigate compression + chunking performance enhancement proposal.
    blob_service.create_blob_from_path(
        container_name=container_name,
        blob_name=blob_name,
        file_path=source,
        progress_callback=lambda c, t: None,
        metadata={'lastmodified': file_time},
        # We want to validate the file as we upload, and only complete the operation
        # if all the data transfers successfully
        validate_content=True,
        max_connections=FileUtils.PARALLEL_OPERATION_THREAD_COUNT)


class FileUtils(object):

    STRIP_PATH = re.compile(r"[/\\]+$")
    GROUP_PREFIX = 'fgrp-'
    MAX_GROUP_LENGTH = 63 - len(GROUP_PREFIX)
    MAX_FILE_SIZE = 50000 * 4 * 1024 * 1024
    PARALLEL_OPERATION_THREAD_COUNT = 5
    SAS_EXPIRY_DAYS = 7  # 7 days
    ROUND_DATE = 2 * 60 * 1000  # Round to nearest 2 minutes

    def __init__(self, client, account_name, resource_group_name, account_endpoint):
        self.resource_file_cache = {}
        self.resolved_storage_client = None
        self.batch_mgmt_client = client
        self.batch_account_name = account_name
        if not self.batch_account_name:
            self.batch_account_name = az_config.get('batch', 'account', None)
        self.batch_account_endpoint = account_endpoint
        if not self.batch_account_endpoint:
            self.batch_account_endpoint = az_config.get('batch', 'endpoint', None)
        self.batch_resource_group = resource_group_name

    def filter_resource_cache(self, container, prefix):
        """Return all blob refeferences in a container cache that meet a prefix requirement."""
        filtered = []
        for blob in self.resource_file_cache[container]:
            if not prefix:
                filtered.append(blob)
            elif blob['filePath'].startswith(prefix):
                filtered.append(blob)
        return filtered

    def list_container_contents(self, source, container, blob_service):
        """List blob references in container."""
        if container not in self.resource_file_cache:
            self.resource_file_cache[container] = []
            blobs = blob_service.list_blobs(container)
            for blob in blobs:
                blob_sas = _generate_blob_sas_token(blob, container, blob_service) \
                    if 'fileGroup' in source else \
                    construct_sas_url(blob, urlsplit(source['containerUrl']))
                file_name = os.path.basename(blob.name)
                file_name_only = os.path.splitext(file_name)[0]
                self.resource_file_cache[container].append(
                    {'url': blob_sas,
                     'filePath': blob.name,
                     'fileName': file_name,
                     'fileNameWithoutExtension': file_name_only})
        return self.filter_resource_cache(container, source.get('prefix'))

    def get_container_sas(self, file_group_name):
        storage_client = self.resolve_storage_account()
        container = _get_container_name(file_group_name)
        return _generate_container_sas_token(container, storage_client)

    def get_container_list(self, source):
        """List blob references in container."""
        storage_client = None
        container = None

        if 'fileGroup' in source:
            # Input data stored in auto-storage
            storage_client = self.resolve_storage_account()
            container = _get_container_name(source['fileGroup'])
        elif 'containerUrl' in source:
            uri = urlsplit(source['containerUrl'])
            if not uri.query:
                raise ValueError('Invalid container url.')
            storage_account_name = uri.netloc.split('.')[0]
            sas_token = uri.query
            storage_client = BlockBlobService(account_name=storage_account_name,
                                              sas_token=sas_token)
            container = uri.pathname.split('/')[1]
        else:
            raise ValueError('Unknown source.')

        return self.list_container_contents(source, container, storage_client)

    def resolve_resource_file(self, resource_file):
        """Convert new resourceFile reference to server-supported reference"""
        if 'blobSource' in resource_file:
            # Support original resourceFile reference
            if 'filePath' not in resource_file:
                raise ValueError('Malformed ResourceFile: \'blobSource\' must '
                                 'also have \'filePath\' attribute')
            return [dict(resource_file)]

        if 'source' not in resource_file:
            raise ValueError('Malformed ResourceFile: Must have either '
                             ' \'source\' or \'blobSource\'')

        storage_client = self.resolve_storage_account()
        container = None
        blobs = []

        if 'fileGroup' in resource_file['source']:
            # Input data stored in auto-storage
            container = _get_container_name(resource_file['source']['fileGroup'])
            blobs = self.list_container_contents(resource_file['source'], container, storage_client)
            return convert_blobs_to_resource_files(blobs, resource_file)
        elif 'containerUrl' in resource_file['source']:
            # Input data storage in arbitrary container
            uri = urlsplit(resource_file['source']['containerUrl'])
            container = uri.pathname.split('/')[1]
            blobs = self.list_container_contents(resource_file['source'], container, storage_client)
            return convert_blobs_to_resource_files(blobs, resource_file)
        elif 'url' in resource_file['source']:
            # TODO: Input data from an arbitrary HTTP GET source
            raise ValueError('Not implemented')
        else:
            raise ValueError('Malformed ResourceFile')

    def resolve_storage_account(self):
        """Resolve Auto-Storage account from supplied Batch Account"""
        if self.resolved_storage_client:
            return self.resolved_storage_client

        if not self.batch_account_name:
            raise ValueError('No Batch account name specified')

        client = self.batch_mgmt_client if self.batch_mgmt_client else \
            get_mgmt_service_client(BatchManagementClient).batch_account

        if self.batch_resource_group:
            # If a resource group was supplied, we can use that to query the Batch Account
            try:
                account = client.get(self.batch_resource_group, self.batch_account_name)
            except CloudError:
                raise ValueError('Couldn\'t find the account named {} in subscription {} '
                                 'with resource group {}'.format(
                                     self.batch_account_name,
                                     client.config.subscription_id,
                                     self.batch_resource_group))
        elif self.batch_account_endpoint:
            # Otherwise, we need to parse the URL for a region in order to identify
            # the Batch account in the subscription
            # Example URL: https://batchaccount.westus.batch.azure.com
            region = urlsplit(self.batch_account_endpoint).netloc.split('.', 2)[1]
            accounts = [x for x in client.list()
                        if x.name == self.batch_account_name and x.location == region]
            try:
                account = accounts[0]
            except IndexError:
                raise ValueError('Couldn\'t find the account named {} in subscription {} '
                                 'in region {}'.format(
                                     self.batch_account_name,
                                     client.config.subscription_id, region))
        else:
            raise ValueError("Insufficient account information. Please supply the account "
                             "name and resource group, or log in to the account with the "
                             "'az batch account login' command.")
        if not account.auto_storage:  # pylint: disable=no-member
            raise ValueError('No linked auto-storage for account {}'
                             .format(self.batch_account_name))  # pylint: disable=no-member

        storage_account_info = account.auto_storage.storage_account_id.split('/')  # pylint: disable=no-member
        storage_resource_group = storage_account_info[4]
        storage_account = storage_account_info[8]

        storage_client = get_mgmt_service_client(StorageManagementClient)
        keys = storage_client.storage_accounts.list_keys(storage_resource_group, storage_account)
        storage_key = keys.keys[0].value  # pylint: disable=no-member

        self.resolved_storage_client = CloudStorageAccount(storage_account, storage_key)\
            .create_block_blob_service()
        return self.resolved_storage_client
