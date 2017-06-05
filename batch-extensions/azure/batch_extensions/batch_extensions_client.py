# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from six.moves.urllib.parse import urlsplit  # pylint: disable=import-error

from msrest.service_client import ServiceClient
from msrest import Serializer, Deserializer
from msrestazure import AzureConfiguration
from .version import VERSION
from .batch_auth import SharedKeyCredentials
from .operations.pool_operations import ExtendedPoolOperations
from .operations.job_operations import ExtendedJobOperations
from .operations.file_operations import ExtendedFileOperations
from azure.batch.operations.application_operations import ApplicationOperations
from azure.batch.operations.account_operations import AccountOperations
from azure.batch.operations.certificate_operations import CertificateOperations
from azure.batch.operations.job_schedule_operations import JobScheduleOperations
from azure.batch.operations.task_operations import TaskOperations
from azure.batch.operations.compute_node_operations import ComputeNodeOperations
from . import models

from azure.common.credentials import get_cli_profile
from azure.batch import BatchServiceClient
from azure.mgmt.batch import BatchManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.storage import CloudStorageAccount


_MGMT_RESOURCE_IDS = {
    'https://batch.core.windows.net/': 'https://management.core.windows.net/',
    'https://batch.chinacloudapi.cn/': 'https://management.core.chinacloudapi.cn/',
    'https://batch.core.usgovcloudapi.net/': 'https://management.core.usgovcloudapi.net/',
    'https://batch.cloudapi.de/': 'https://management.core.cloudapi.de/',
}


class BatchExtensionsClient(BatchServiceClient):
    """A client for issuing REST requests to the Azure Batch service.

    :ivar config: Configuration for client.
    :vartype config: BatchServiceClientConfiguration

    :ivar pool: Pool operations
    :vartype pool: .operations.PoolOperations
    :ivar account: Account operations
    :vartype account: .operations.AccountOperations
    :ivar job: Job operations
    :vartype job: .operations.JobOperations
    :ivar file: File operations
    :vartype file: .operations.FileOperations
    :ivar task: Task operations
    :vartype task: .operations.TaskOperations

    :param credentials: Credentials needed for the client to connect to Azure.
    :type credentials: :mod:`A msrestazure Credentials
     object<msrestazure.azure_active_directory>`
    :param api_version: Client API Version.
    :type api_version: str
    :param str base_url: Service URL
    """

    def __init__(self, credentials=None, base_url=None, subscription_id=None,
            resource_group=None, batch_account=None, storage_client=None):
        if not credentials:
            try:
                profile = get_cli_profile()
                subscription = profile.get_expanded_subscription_info(
                    subscription_id=subscription_id)
                resource = subscription['endpoints'].batch_resource_id
                credentials, subscription_id, _ = profile.get_login_credentials(
                    resource=resource, subscription_id=subscription['subscriptionId'])
            except ImportError:
                raise ValueError('Unable to load Azure CLI authenticated session. Please '
                                 'supply credentials.')
        super(BatchExtensionsClient, self).__init__(credentials, base_url=base_url)
        self.config.add_user_agent('batchextensionsclient/{}'.format(VERSION))
        self._mgmt_client = None
        self._resolved_storage_client = storage_client
        self._subscription = subscription_id

        self.batch_account = batch_account
        self.resource_group = resource_group

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.pool = ExtendedPoolOperations(
            self, self._client, self.config, self._serialize, self._deserialize, self._storage_account)
        self.job = ExtendedJobOperations(
            self, self._client, self.config, self._serialize, self._deserialize, self._storage_account)
        self.file = ExtendedFileOperations(
            self, self._client, self.config, self._serialize, self._deserialize, self._storage_account)
        self.application = ApplicationOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.account = AccountOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.certificate = CertificateOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.job_schedule = JobScheduleOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.task = TaskOperations(
            self._client, self.config, self._serialize, self._deserialize)
        self.compute_node = ComputeNodeOperations(
            self._client, self.config, self._serialize, self._deserialize)

    def _storage_account(self):
        """Resolve Auto-Storage account from supplied Batch Account"""
        if self._resolved_storage_client:
            return self._resolved_storage_client
        if not self._subscription or not self.batch_account:
            raise ValueError("Unable to resolve auto-storage account without "
                             "subscription ID and Batch account name.")

        if self._mgmt_client:
            client = self._mgmt_client
            credentials = client.config.credentials
        else:
            try:
                from azure.common.client_factory import get_client_from_cli_profile
                client = get_client_from_cli_profile(BatchManagementClient, 
                    subscription_id=self._subscription)
                self._mgmt_client = client
                credentials = client.config.credentials
            except ImportError:
                try:
                    credentials = self.config.credentials
                    credentials._resource = _MGMT_RESOURCE_IDS.get(credentials._resource)
                    client = BatchManagementClient(credentials, self._subscription)
                except AttributeError:
                    raise ValueError("Unable to resolve auto-storage account because the"
                                     "client is not authenticated using a AAD credentials.")
                except KeyError:
                    raise ValueError("Unable to resolve auto-storage account because the"
                                     "client is authenticated with an unknown resource: "
                                     "{}".format(self.config.credentials._resource))

        if self.resource_group:
            # If a resource group was supplied, we can use that to query the Batch Account
            try:
                account = client.batch_account.get(self.resource_group, self.batch_account)
            except Exception:
                raise ValueError('Couldn\'t find the account named {} in subscription {} '
                                 'with resource group {}'.format(
                                     self.batch_account, self._subscription, self.resource_group))
        else:
            # Otherwise, we need to parse the URL for a region in order to identify
            # the Batch account in the subscription
            # Example URL: https://batchaccount.westus.batch.azure.com
            region = urlsplit(self.config.base_url).netloc.split('.', 2)[1]
            accounts = [x for x in client.batch_account.list()
                        if x.name == self.batch_account and x.location == region]
            try:
                account = accounts[0]
            except IndexError:
                raise ValueError('Couldn\'t find the account named {} in subscription {} '
                                 'in region {}'.format(
                                     self.batch_account, self._subscription, region))
        if not account.auto_storage:
            raise ValueError('No linked auto-storage for account {}'.format(self.batch_account))

        storage_account_info = account.auto_storage.storage_account_id.split('/')  # pylint: disable=no-member
        storage_resource_group = storage_account_info[4]
        storage_account = storage_account_info[8]
        storage_client = StorageManagementClient(credentials, self._subscription)
        keys = storage_client.storage_accounts.list_keys(storage_resource_group, storage_account)
        storage_key = keys.keys[0].value  # pylint: disable=no-member

        self.resolved_storage_client = CloudStorageAccount(storage_account, storage_key)\
            .create_block_blob_service()
        return self.resolved_storage_client

