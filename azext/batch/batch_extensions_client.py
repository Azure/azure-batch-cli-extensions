# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import copy

from six.moves.urllib.parse import urlsplit  # pylint: disable=import-error,relative-import
from msrest import Serializer, Deserializer

from azure.batch import BatchServiceClient
from azure.mgmt.batch import BatchManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.multiapi.storage.v2018_11_09.blob import BlockBlobService
from azure.common.credentials import get_cli_profile

from .version import VERSION
from .operations.pool_operations import ExtendedPoolOperations
from .operations.job_operations import ExtendedJobOperations
from .operations.file_operations import ExtendedFileOperations
from . import models

# pylint: disable=protected-access


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
    :param str batch_url: Batch Service URL
    :param str mgmt_base_uri: Management Service URL
    :param str storage_enpoint: Storage Endpoint Suffix
    """

    def __init__(self, credentials=None, batch_url=None, subscription_id=None,
                 resource_group=None, batch_account=None, storage_client=None,
                 storage_endpoint=None, mgmt_credentials=None, mgmt_base_url="https://management.azure.com"):
        credentials, mgmt_credentials, subscription_id = self._configure_credentials(
            credentials, mgmt_credentials, subscription_id)
        super(BatchExtensionsClient, self).__init__(credentials, batch_url=batch_url)
        self.config.add_user_agent('batchextensionsclient/{}'.format(VERSION))
        self._batch_url = batch_url
        if self._batch_url:
            self._batch_url = self._batch_url.rstrip('/')
        self._mgmt_client = None
        self._mgmt_credentials = mgmt_credentials
        self._mgmt_base_url = mgmt_base_url
        if self._mgmt_base_url:
            self._mgmt_base_url = self._mgmt_base_url.rstrip('/')
        self._resolved_storage_client = storage_client
        self._subscription = subscription_id
        self._storage_endpoint = storage_endpoint

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

    def _get_cli_profile(self, subscription_id):  # pylint:disable=no-self-use
        try:
            from azure.cli.core.util import CLIError
            from azure.cli.core.cloud import get_active_cloud
            try:
                profile = get_cli_profile()
                cloud = get_active_cloud()
                subscription = profile.get_subscription(subscription=subscription_id)
                return profile, subscription['id'], cloud.endpoints
            except CLIError:
                raise ValueError("Unable to load Azure CLI authenticated session. Please "
                                 "run the 'az login' command or supply an AAD credentials "
                                 "object from azure.common.credentials.")
        except ImportError:
            raise ValueError('Unable to load Azure CLI authenticated session. Please '
                             'supply an AAD credentials object from azure.common.credentials')
        except (AttributeError, KeyError, TypeError) as error:
            raise ValueError('Unable to load Azure CLI authenticated session. There is '
                             'a version conflict with azure-cli-core. Please check for '
                             'updates or report this issue at '
                             'github.com/Azure/azure-batch-cli-extensions:\n{}'.format(str(error)))

    def _configure_credentials(self, credentials, mgmt_credentials, subscription_id):
        if not credentials:
            from azure.cli.core.util import in_cloud_console
            profile, subscription, endpoints = self._get_cli_profile(subscription_id)
            if in_cloud_console():
                resource = endpoints.active_directory_resource_id
            else:
                resource = endpoints.batch_resource_id
            credentials, subscription_id, _ = profile.get_login_credentials(
                resource=resource, subscription_id=subscription)

        if not mgmt_credentials:
            try:
                profile, subscription, endpoints = self._get_cli_profile(subscription_id)
            except ValueError:
                pass
            else:
                mgmt_credentials, subscription_id, _ = profile.get_login_credentials(
                    resource=endpoints.management, subscription_id=subscription)

        if not mgmt_credentials:
            try:
                mgmt_resource = credentials.cloud_environment.endpoints.management
            except AttributeError:
                pass
            else:
                mgmt_credentials = copy.copy(credentials)
                mgmt_credentials.resource = mgmt_resource
                mgmt_credentials.set_token()
        return credentials, mgmt_credentials, subscription_id

    def _storage_account(self):
        """Resolve Auto-Storage account from supplied Batch Account"""
        if self._resolved_storage_client:
            return self._resolved_storage_client
        if not self._subscription or not self.batch_account:
            raise ValueError("Unable to resolve auto-storage account without "
                             "subscription ID and Batch account name.")
        if not self._mgmt_credentials:
            raise ValueError("Unable to resolve auto-storage account without "
                             "Management AAD Credentials.")
        if self._mgmt_client:
            client = self._mgmt_client
        else:
            client = BatchManagementClient(self._mgmt_credentials,
                                           self._subscription,
                                           base_url=self._mgmt_base_url)
            self._mgmt_client = client

        if self.resource_group:
            # If a resource group was supplied, we can use that to query the Batch Account
            try:
                account = client.batch_account.get(self.resource_group, self.batch_account)
            except Exception:
                raise ValueError("Couldn't find the account named '{}' in subscription '{}' "
                                 "with resource group '{}'".format(
                                     self.batch_account, self._subscription, self.resource_group))
        else:
            # Otherwise, we need to parse the URL for a region in order to identify
            # the Batch account in the subscription
            # Example URL: https://batchaccount.westus.batch.azure.com
            region = urlsplit(self.config.batch_url).netloc.split('.', 2)[1]
            accounts = (x for x in client.batch_account.list()
                        if x.name == self.batch_account and x.location == region)
            try:
                account = next(accounts)
            except StopIteration:
                raise ValueError("Couldn't find the account named '{}' in subscription '{}' "
                                 "in region '{}'".format(
                                     self.batch_account, self._subscription, region))
        if not account.auto_storage:  # pylint: disable=no-member
            raise ValueError("No linked auto-storage for account '{}'".format(self.batch_account))

        storage_account_info = account.auto_storage.storage_account_id.split('/')  # pylint: disable=no-member
        storage_resource_group = storage_account_info[4]
        storage_account = storage_account_info[8]
        storage_client = StorageManagementClient(self._mgmt_credentials,
                                                 self._subscription,
                                                 base_url=self._mgmt_base_url)
        keys = storage_client.storage_accounts.list_keys(storage_resource_group, storage_account)
        storage_key = keys.keys[0].value  # pylint: disable=no-member

        self._resolved_storage_client = BlockBlobService(account_name=storage_account,
                                                         account_key=storage_key,
                                                         endpoint_suffix=self._storage_endpoint)
        return self._resolved_storage_client
