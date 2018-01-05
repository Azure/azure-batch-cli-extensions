# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core import AzCommandsLoader
from azure.cli.command_modules.batch._exception_handler import batch_exception_handler
from azext_batch._client_factory import batch_extensions_client
import azext_batch._help  # pylint: disable=unused-import
from azext_batch.version import VERSION


class BatchExtensionsCommandLoader(AzCommandsLoader):

    def __init__(self, cli_ctx=None):
        from azure.cli.core.commands import CliCommandType
        batch_ext_custom = CliCommandType(
            operations_tmpl='azext_batch.custom#{}',
            client_factory=batch_extensions_client,
            exception_handler=batch_exception_handler)
        super(BatchExtensionsCommandLoader, self).__init__(
            cli_ctx=cli_ctx,
            custom_command_type=batch_ext_custom)
        self.module_name = __name__

    def load_command_table(self, args):
        super(BatchExtensionsCommandLoader, self).load_command_table(args)
        from azext_batch.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        super(BatchExtensionsCommandLoader, self).load_arguments(command)
        from azext_batch._params import load_arguments
        load_arguments(self, command)


__version__ = VERSION
COMMAND_LOADER_CLS = BatchExtensionsCommandLoader
