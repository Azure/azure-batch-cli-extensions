# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.commands import cli_command

from azure.cli.command_modules.batch_extensions._client_factory import (
    account_mgmt_client_factory, batch_data_service_factory)

custom_path = 'azure.cli.command_modules.batch_extensions.custom#{}'

# pylint: disable=line-too-long
# NCJ Commands

cli_command(__name__, 'batch file upload', custom_path.format('upload_file'), account_mgmt_client_factory)
cli_command(__name__, 'batch file download', custom_path.format('download_file'), account_mgmt_client_factory)

cli_command(__name__, 'batch pool create', custom_path.format('create_pool'), batch_data_service_factory)
cli_command(__name__, 'batch job create', custom_path.format('create_job'), batch_data_service_factory)
