# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from argcomplete.completers import FilesCompleter

from azure.cli.core.commands import \
    (register_cli_argument, CliArgumentType, register_extra_cli_argument)
from azure.cli.core.commands.parameters import \
    (resource_group_name_type,
     get_resource_name_completion_list, file_type)

from azure.cli.command_modules.batch_extensions._validators import \
    (validate_pool_settings, validate_client_parameters, metadata_item_format,
     certificate_reference_format, validate_json_file, load_node_agent_skus)

# pylint: disable=line-too-long
# ARGUMENT DEFINITIONS

batch_name_type = CliArgumentType(help='Name of the Batch account.', options_list=('--account-name',), completer=get_resource_name_completion_list('Microsoft.Batch/batchAccounts'), id_part=None)

# PARAMETER REGISTRATIONS


register_cli_argument('batch pool create', 'json_file', type=file_type, help='The file containing the pool to create in JSON format, if this parameter is specified, all other parameters are ignored.', validator=validate_json_file, completer=FilesCompleter())
register_cli_argument('batch pool create', 'id', help='The ID of the pool to be updated.', validator=validate_pool_settings)
register_cli_argument('batch pool create', 'application_package_references', nargs='+')  # type=application_package_reference_format)
register_cli_argument('batch pool create', 'certificate_references', nargs='+', type=certificate_reference_format)
register_cli_argument('batch pool create', 'metadata', nargs='+', type=metadata_item_format)
register_cli_argument('batch pool create', 'image', completer=load_node_agent_skus, arg_group="Pool: Virtual Machine Configuration",
                      help="OS image URN in 'publisher:offer:sku[:version]' format. Version is optional and if omitted latest will be used.\n\tValues from 'az batch pool node-agent-skus list'.\n\tExample: 'MicrosoftWindowsServer:WindowsServer:2012-R2-Datacenter:latest'")
register_cli_argument('batch pool create', 'account_name', arg_group='Batch Account',
                      validator=validate_client_parameters,
                      help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch pool create', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_cli_argument('batch pool create', 'account_endpoint', arg_group='Batch Account',
                      help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')

register_cli_argument('batch job create', 'account_name', arg_group='Batch Account',
                      validator=validate_client_parameters,
                      help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch job create', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_cli_argument('batch job create', 'account_endpoint', arg_group='Batch Account',
                      help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')

register_cli_argument('batch file upload', 'resource_group', resource_group_name_type, completer=None, required=False)
register_cli_argument('batch file upload', 'account_name', batch_name_type, options_list=('--name', '-n'), required=False)
register_cli_argument('batch file upload', 'local_path', type=file_type, help='Path to a local file or directory to be uploaded - can include wildcard patterns.')
register_cli_argument('batch file upload', 'file_group', help='Name of a file group under which the files will be stored.')
register_cli_argument('batch file upload', 'remote_path', help='Group subdirectory under which files will be uploaded.')
register_cli_argument('batch file upload', 'flatten', action='store_true', help='If set, will not retain local directory structure in storage.')

register_cli_argument('batch file download', 'resource_group', resource_group_name_type, completer=None, required=False)
register_cli_argument('batch file download', 'account_name', batch_name_type, options_list=('--name', '-n'), required=False)
register_cli_argument('batch file download', 'local_path', type=file_type, help='Path to a local file or directory to be stored the download files.')
register_cli_argument('batch file download', 'file_group', help='Name of a file group under which the files will be download.')
register_cli_argument('batch file download', 'remote_path', help='The subdirectory under which files exist remotely.')
register_cli_argument('batch file download', 'overwrite', action='store_true', help='If set, an existing file in the local path will be overwritten.')
