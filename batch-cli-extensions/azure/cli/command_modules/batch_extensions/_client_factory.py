# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.batch_extensions as batch


def batch_extensions_client(kwargs):
    account_name = kwargs.pop('account_name', None)
    account_endpoint = kwargs.pop('account_endpoint', None)
    resource_group = kwargs.pop('resource_group', None)
    client = batch.BatchExtensionsClient(base_url=account_endpoint)
    client.resource_group = resource_group
    client.batch_account = account_name
    kwargs.pop('account_key', None)
    return client
