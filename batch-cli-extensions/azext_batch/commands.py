# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from distutils import version  # pylint: disable=no-name-in-module

from knack.log import get_logger

from azure.batch import __version__ as batch_version
from azure.mgmt.batch import __version__ as batch_mgmt_version
from azext.batch import __version__ as batch_ext_version


logger = get_logger(__name__)
SUPPORTED_BATCH_VERSION = "5.2"
SUPPORTED_BMGMT_VERSION = "5.1"
SUPPORTED_BATCH_EXT_VERSION = "4.1"


def confirm_version(current, supported, package):
    if version.StrictVersion(current) >= version.StrictVersion(supported):
        logger.warning("This package of the Batch Extensions module supports "
                       "%s up to version %s. The current version %s has not been "
                       "tested for compatibility.", package, supported, current)

confirm_version(batch_version, SUPPORTED_BATCH_VERSION, "Azure Batch")
confirm_version(batch_mgmt_version, SUPPORTED_BMGMT_VERSION, "Azure Batch Management")
confirm_version(batch_ext_version, SUPPORTED_BATCH_EXT_VERSION, "Azure Batch Extensions")


def load_command_table(self, _):

    with self.command_group('batch file') as g:
        g.custom_command('upload', 'upload_file')
        g.custom_command('download', 'download_file')

    with self.command_group('batch pool') as g:
        g.custom_command('create', 'create_pool')

    with self.command_group('batch job') as g:
        g.custom_command('create', 'create_job')
