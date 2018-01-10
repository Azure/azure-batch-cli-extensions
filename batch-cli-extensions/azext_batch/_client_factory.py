# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def batch_extensions_client(cli_ctx, kwargs):  # pylint: disable=unused-argument
    from knack.util import CLIError
    import azure.batch_extensions as batch

    account_name = kwargs.pop('account_name', None)
    account_endpoint = kwargs.pop('account_endpoint', None)
    resource_group = kwargs.pop('resource_group', None)
    if account_endpoint and not account_endpoint.startswith('https://'):
        account_endpoint = 'https://' + account_endpoint
    try:
        client = batch.BatchExtensionsClient(base_url=account_endpoint)
    except ValueError as error:
        raise CLIError(str(error))
    client.resource_group = resource_group
    client.batch_account = account_name
    kwargs.pop('account_key', None)
    return client
