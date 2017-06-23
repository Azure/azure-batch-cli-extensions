# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azure.cli.command_modules.batch_extensions._help  # pylint: disable=unused-import
from .version import VERSION


def load_params(_):
    import azure.cli.command_modules.batch_extensions._params  # pylint: disable=unused-variable,redefined-outer-name


def load_commands():
    import azure.cli.command_modules.batch_extensions.commands  # pylint: disable=unused-variable,redefined-outer-name

__version__ = VERSION
