# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import azext_batch._help  # pylint: disable=unused-import
from .version import VERSION


def load_params(_):
    import azext_batch._params  # pylint: disable=unused-variable,redefined-outer-name


def load_commands():
    import azext_batch.commands  # pylint: disable=unused-variable,redefined-outer-name

__version__ = VERSION
