# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.mgmt.batch import BatchManagementClient

import azure.batch_extensions.batch_extensions_client as batch
import azure.batch_extensions.batch_auth as batchauth

from azure.cli.core.commands.client_factory import get_mgmt_service_client


def batch_extensions_client(kwargs):
    from azure.cli.core._profile import Profile, CLOUD
    account_name = kwargs.pop('account_name', None)
    account_key = kwargs.pop('account_key', None)
    account_endpoint = kwargs.pop('account_endpoint', None)
    resource_group = kwargs.pop('resource_group', None)
    client = batch.BatchExtensionsClient(base_url=account_endpoint)
    client.resource_group = resource_group
    client.batch_account = account_name
    return client
