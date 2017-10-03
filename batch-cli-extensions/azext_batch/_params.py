# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from argcomplete.completers import FilesCompleter

from azure.cli.core.commands import \
    (register_cli_argument, CliArgumentType, register_extra_cli_argument)
from azure.cli.core.commands.parameters import \
    (get_resource_name_completion_list, file_type)

from azext_batch._validators import \
    (validate_pool_settings, validate_client_parameters, metadata_item_format, environment_setting_format,
     certificate_reference_format, validate_json_file, load_node_agent_skus, resource_file_format)

# pylint: disable=line-too-long
# ARGUMENT DEFINITIONS

batch_name_type = CliArgumentType(help='Name of the Batch account.', options_list=('--account-name',), completer=get_resource_name_completion_list('Microsoft.Batch/batchAccounts'), id_part=None)

# PARAMETER REGISTRATIONS


# Pool Create
register_cli_argument('batch pool create', 'json_file', type=file_type, help='The file containing the pool to create in JSON format, if this parameter is specified, all other parameters are ignored.', validator=validate_json_file, completer=FilesCompleter())
register_cli_argument('batch pool create', 'template', type=file_type, arg_group='Batch Extensions', help='A Batch pool JSON template file. If this parameter is specified, all other parameters are ignored.', completer=FilesCompleter())
register_cli_argument('batch pool create', 'parameters', type=file_type, arg_group='Batch Extensions', help='Parameter values for a Batch pool JSON template file. Can only be used with --template.', completer=FilesCompleter())
register_cli_argument('batch pool create', 'application_package_references', nargs='+', validator=validate_pool_settings)
register_cli_argument('batch pool create', 'certificate_references', nargs='+', type=certificate_reference_format)
register_cli_argument('batch pool create', 'application_licenses', nargs='+')
register_cli_argument('batch pool create', 'metadata', nargs='+', type=metadata_item_format)
register_cli_argument('batch pool create', 'start_task_command_line', arg_group='Pool: Start Task', help='The command line of the start task. The command line does not run under a shell, and therefore cannot take advantage of shell features such as environment variable expansion. If you want to take advantage of such features, you should invoke the shell in the command line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c MyCommand" in Linux.')
register_cli_argument('batch pool create', 'start_task_resource_files', arg_group='Pool: Start Task', nargs='+', type=resource_file_format, help='A list of files that the Batch service will download to the compute node before running the command line. Space separated resource references in filename=blobsource format.')
register_cli_argument('batch pool create', 'start_task_wait_for_success', arg_group='Pool: Start Task', action='store_true', help='Whether the Batch service should wait for the start task to complete successfully (that is, to exit with exit code 0) before scheduling any tasks on the compute node. If true and the start task fails on a compute node, the Batch service retries the start task up to its maximum retry count (maxTaskRetryCount). If the task has still not completed successfully after all retries, then the Batch service marks the compute node unusable, and will not schedule tasks to it. This condition can be detected via the node state and scheduling error detail. If false, the Batch service will not wait for the start task to complete. In this case, other tasks can start executing on the compute node while the start task is still running; and even if the start task fails, new tasks will continue to be scheduled on the node. The default is false. True if flag present.')
register_cli_argument('batch pool create', 'os_family', arg_group="Pool: Cloud Service Configuration",
                      help='The Azure Guest OS family to be installed on the virtual machines in the pool. Possible values are: 2 - OS Family 2, equivalent to Windows Server 2008 R2 SP1. 3 - OS Family 3, equivalent to Windows Server 2012. 4 - OS Family 4, equivalent to Windows Server 2012 R2. 5 - OS Family 5, equivalent to Windows Server 2016. For more information, see Azure Guest OS Releases (https://azure.microsoft.com/documentation/articles/cloud-services-guestos-update-matrix/#releases). Allowed values: 2, 3, 4, 5.')
register_cli_argument('batch pool create', 'node_agent_sku_id', arg_group="Pool: Virtual Machine Configuration", help='The SKU of the Batch node agent to be provisioned on compute nodes in the pool. The Batch node agent is a program that runs on each node in the pool, and provides the command-and-control interface between the node and the Batch service. There are different implementations of the node agent, known as SKUs, for different operating systems. You must specify a node agent SKU which matches the selected image reference. To get the list of supported node agent SKUs along with their list of verified image references, see the \'List supported node agent SKUs\' operation.')
register_cli_argument('batch pool create', 'image', completer=load_node_agent_skus, arg_group="Pool: Virtual Machine Configuration",
                      help="OS image URN in 'publisher:offer:sku[:version]' format. Version is optional and if omitted latest will be used.\n\tValues from 'az batch pool node-agent-skus list'.\n\tExample: 'MicrosoftWindowsServer:WindowsServer:2012-R2-Datacenter:latest'")
register_extra_cli_argument('batch pool create', 'account_name', arg_group='Batch Account', validator=validate_client_parameters,
                            help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch pool create', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_extra_cli_argument('batch pool create', 'account_endpoint', arg_group='Batch Account',
                            help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')
register_extra_cli_argument('batch pool create', 'resource_group', arg_group='Batch Account', help='The resource group of the Batch account')

# Job Create
register_cli_argument('batch job create', 'json_file', type=file_type, help='The file containing the job to create in JSON format, if this parameter is specified, all other parameters are ignored.', validator=validate_json_file, completer=FilesCompleter())
register_cli_argument('batch job create', 'template', type=file_type, arg_group='Batch Extensions', help='A Batch job JSON template file. If this parameter is specified, all other parameters are ignored.', completer=FilesCompleter())
register_cli_argument('batch job create', 'parameters', type=file_type, arg_group='Batch Extensions', help='Parameter values for a Batch job JSON template file. Can only be used with --template.', completer=FilesCompleter())
register_cli_argument('batch job create', 'metadata', nargs='+', type=metadata_item_format, help='A list of name-value pairs associated with the job as metadata. The Batch service does not assign any meaning to metadata; it is solely for the use of user code. Space separated values in \'key=value\' format.')
register_cli_argument('batch job create', 'uses_task_dependencies', action='store_true', help='The flag that determines if this job will use tasks with dependencies. True if flag present.')
register_cli_argument('batch job create', 'pool_id', arg_group='Job: Pool Info', help='The id of an existing pool. All the tasks of the job will run on the specified pool.')
register_cli_argument('batch job create', 'job_max_task_retry_count', arg_group='Job: Constraints', help='The maximum number of times each task may be retried. The Batch service retries a task if its exit code is nonzero. Note that this value specifically controls the number of retries. The Batch service will try each task once, and may then retry up to this limit. For example, if the maximum retry count is 3, Batch tries a task up to 4 times (one initial try and 3 retries). If the maximum retry count is 0, the Batch service does not retry tasks. If the maximum retry count is -1, the Batch service retries tasks without limit. The default value is 0 (no retries).')
register_cli_argument('batch job create', 'job_max_wall_clock_time', arg_group='Job: Constraints', help='The maximum elapsed time that the job may run, measured from the time the job is created. If the job does not complete within the time limit, the Batch service terminates it and any tasks that are still running. In this case, the termination reason will be MaxWallClockTimeExpiry. If this property is not specified, there is no time limit on how long the job may run. Expected format is an ISO-8601 duration.')
register_cli_argument('batch job create', 'job_manager_task_command_line', arg_group='Job: Job Manager Task', help='The command line of the Job Manager task. The command line does not run under a shell, and therefore cannot take advantage of shell features such as environment variable expansion. If you want to take advantage of such features, you should invoke the shell in the command line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c MyCommand" in Linux.')
register_cli_argument('batch job create', 'job_manager_task_environment_settings', arg_group='Job: Job Manager Task', type=environment_setting_format, help='A list of environment variable settings for the Job Manager task. Space separated values in \'key=value\' format.')
register_cli_argument('batch job create', 'job_manager_task_resource_files', arg_group='Job: Job Manager Task', type=resource_file_format, help='A list of files that the Batch service will download to the compute node before running the command line. Files listed under this element are located in the task\'s working directory. Space separated resource references in filename=blobsource format.')
register_cli_argument('batch job create', 'job_manager_task_id', arg_group='Job: Job Manager Task', help='A string that uniquely identifies the Job Manager task within the job. The id can contain any combination of alphanumeric characters including hyphens and underscores and cannot contain more than 64 characters.')
register_extra_cli_argument('batch job create', 'account_name', arg_group='Batch Account', validator=validate_client_parameters,
                            help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch job create', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_extra_cli_argument('batch job create', 'account_endpoint', arg_group='Batch Account',
                            help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')
register_extra_cli_argument('batch job create', 'resource_group', arg_group='Batch Account', help='The resource group of the Batch account')

# File Upload
register_cli_argument('batch file upload', 'local_path', type=file_type, help='Path to a local file or directory to be uploaded - can include wildcard patterns.')
register_cli_argument('batch file upload', 'file_group', help='Name of a file group under which the files will be stored.')
register_cli_argument('batch file upload', 'remote_path', help='Group subdirectory under which files will be uploaded.')
register_cli_argument('batch file upload', 'flatten', action='store_true', help='If set, will not retain local directory structure in storage.')
register_extra_cli_argument('batch file upload', 'account_name', arg_group='Batch Account', validator=validate_client_parameters,
                            help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch file upload', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_extra_cli_argument('batch file upload', 'account_endpoint', arg_group='Batch Account',
                            help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')
register_extra_cli_argument('batch file upload', 'resource_group', arg_group='Batch Account', help='The resource group of the Batch account')

# File Download
register_cli_argument('batch file download', 'local_path', type=file_type, help='Path to a local file or directory to be stored the download files.')
register_cli_argument('batch file download', 'file_group', help='Name of a file group from which the files will be downloaded.')
register_cli_argument('batch file download', 'remote_path', help='The subdirectory under which files exist remotely.')
register_cli_argument('batch file download', 'overwrite', action='store_true', help='If set, an existing file in the local path will be overwritten.')
register_extra_cli_argument('batch file download', 'account_name', arg_group='Batch Account', validator=validate_client_parameters,
                            help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
register_extra_cli_argument('batch file download', 'account_key', arg_group='Batch Account',
                            help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
register_extra_cli_argument('batch file download', 'account_endpoint', arg_group='Batch Account',
                            help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')
register_extra_cli_argument('batch file download', 'resource_group', arg_group='Batch Account', help='The resource group of the Batch account')
