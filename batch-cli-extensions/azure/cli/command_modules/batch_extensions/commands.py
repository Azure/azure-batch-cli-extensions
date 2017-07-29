# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from distutils import version  # pylint: disable=no-name-in-module

from azure.cli.core import __version__ as core_version
from azure.cli.core.commands import cli_command
import azure.cli.core.azlogging as azlogging

from azure.batch import __version__ as batch_version
from azure.mgmt.batch import __version__ as batch_mgmt_version
#from azure.cli.batch import __version__ as batch_cli_version

from azure.cli.command_modules.batch_extensions._client_factory import (
    batch_extensions_client)


logger = azlogging.get_az_logger(__name__)
SUPPORTED_CORE_VERSION = "2.1"
SUPPORTED_BATCH_VERSION = "3.2"
SUPPORTED_BMGMT_VERSION = "4.2"


def confirm_version(current, supported, package):
    if version.StrictVersion(current) >= version.StrictVersion(supported):
        logger.warning("This package of the Batch Extensions module supports "
                       "%s up to version %s. The current version %s has not been "
                       "tested for compatibility.", package, supported, current)

confirm_version(core_version, SUPPORTED_CORE_VERSION, "Azure CLI Core")
confirm_version(batch_version, SUPPORTED_BATCH_VERSION, "Azure Batch")
confirm_version(batch_mgmt_version, SUPPORTED_BMGMT_VERSION, "Azure Batch Management")
#confirm_version(batch_cli_version, SUPPORTED_CORE_VERSION, "Azure Batch CLI")

custom_path = 'azure.cli.command_modules.batch_extensions.custom#{}'

# pylint: disable=line-too-long
# NCJ Commands

cli_command(__name__, 'batch file upload', custom_path.format('upload_file'), batch_extensions_client)
cli_command(__name__, 'batch file download', custom_path.format('download_file'), batch_extensions_client)
cli_command(__name__, 'batch pool create', custom_path.format('create_pool'), batch_extensions_client)
cli_command(__name__, 'batch job create', custom_path.format('create_job'), batch_extensions_client)
