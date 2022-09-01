# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from argcomplete.completers import FilesCompleter

from azure.cli.core.commands.parameters import file_type
from azure.cli.command_modules.batch._completers import load_supported_images
from azure.cli.command_modules.batch._validators import (
    metadata_item_format, certificate_reference_format, validate_json_file,
    environment_setting_format, resource_file_format)
from azext_batch._validators import validate_pool_settings, validate_client_parameters


# pylint: disable=line-too-long, too-many-statements
def load_arguments(self, _):

    with self.argument_context('batch pool create') as c:
        c.argument('json_file', type=file_type, help='The file containing the pool to create in JSON format, if this parameter is specified, all other parameters are ignored.', validator=validate_json_file, completer=FilesCompleter())
        c.argument('template', type=file_type, arg_group='Batch Extensions', help='A Batch pool JSON template file. If this parameter is specified, all other parameters are ignored.', completer=FilesCompleter())
        c.argument('parameters', type=file_type, arg_group='Batch Extensions', help='Parameter values for a Batch pool JSON template file. Can only be used with --template.', completer=FilesCompleter())
        c.argument('os_version', arg_group='Pool: Cloud Service Configuration', help='The default value is * which specifies the latest operating system version for the specified OS family.')
        c.argument('certificate_references', nargs='+', type=certificate_reference_format)
        c.argument('metadata', nargs='+', type=metadata_item_format)
        c.argument('start_task_command_line', arg_group='Pool: Start Task', help='The command line of the start task. The command line does not run under a shell, and therefore cannot take advantage of shell features such as environment variable expansion. If you want to take advantage of such features, you should invoke the shell in the command line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c MyCommand" in Linux.')
        c.argument('start_task_resource_files', arg_group='Pool: Start Task', nargs='+', type=resource_file_format, help='A list of files that the Batch service will download to the compute node before running the command line. Space separated resource references in filename=httpurl format.')
        c.argument('start_task_wait_for_success', arg_group='Pool: Start Task', action='store_true', help='Whether the Batch service should wait for the start task to complete successfully (that is, to exit with exit code 0) before scheduling any tasks on the compute node. If true and the start task fails on a compute node, the Batch service retries the start task up to its maximum retry count (maxTaskRetryCount). If the task has still not completed successfully after all retries, then the Batch service marks the compute node unusable, and will not schedule tasks to it. This condition can be detected via the node state and scheduling error detail. If false, the Batch service will not wait for the start task to complete. In this case, other tasks can start executing on the compute node while the start task is still running; and even if the start task fails, new tasks will continue to be scheduled on the node. The default is false. True if flag present.')
        c.argument('os_family', arg_group="Pool: Cloud Service Configuration",
                   help='The Azure Guest OS family to be installed on the virtual machines in the pool. Possible values are: 2 - OS Family 2, equivalent to Windows Server 2008 R2 SP1. 3 - OS Family 3, equivalent to Windows Server 2012. 4 - OS Family 4, equivalent to Windows Server 2012 R2. 5 - OS Family 5, equivalent to Windows Server 2016. For more information, see Azure Guest OS Releases (https://azure.microsoft.com/documentation/articles/cloud-services-guestos-update-matrix/#releases). Allowed values: 2, 3, 4, 5.')
        c.extra('disk_encryption_targets',
                arg_group="Pool: Virtual Machine Configuration",
                help='A space seperated list of DiskEncryptionTargets. current possible values include OsDisk and TemporaryDisk.')
        c.extra('disk_encryption_configuration_targets', options_list=('--targets',),
                arg_group="Pool: Virtual Machine Configuration: Disk Encryption Configuration Arguments",
                help='If omitted, no disks on the compute nodes in the pool will be encrypted. On Linux pool, only "TemporaryDisk" is supported; on Windows pool, "OsDisk" and "TemporaryDisk" must be specified. Space seperated target disks to be encrypted. Values can either be OsDisk or TemporaryDisk.')
        c.extra('node_placement_policy', options_list=('--policy',),
                arg_group="Pool: Virtual Machine Configuration: Node Placement Configuration Arguments",
                help='Node placement Policy type on Batch Pools. Allocation policy used by Batch Service to provision the nodes. If not specified, Batch will use the regional policy.  Allowed values: regional, zonal.')
        c.argument('node_agent_sku_id', arg_group="Pool: Virtual Machine Configuration", help='The SKU of the Batch node agent to be provisioned on compute nodes in the pool. The Batch node agent is a program that runs on each node in the pool, and provides the command-and-control interface between the node and the Batch service. There are different implementations of the node agent, known as SKUs, for different operating systems. You must specify a node agent SKU which matches the selected image reference. To get the list of supported node agent SKUs along with their list of verified image references, see the \'List supported node agent SKUs\' operation.')
        c.argument('image', completer=load_supported_images, arg_group="Pool: Virtual Machine Configuration",
                   help="OS image reference. This can be either 'publisher:offer:sku[:version]' format, or a fully qualified ARM image id of the form '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/images/{imageName}'. If 'publisher:offer:sku[:version]' format, version is optional and if omitted latest will be used. Valid values can be retrieved via 'az batch pool node-agent-skus list'. For example: 'MicrosoftWindowsServer:WindowsServer:2012-R2-Datacenter:latest'")

    with self.argument_context('batch job create') as c:
        c.argument('json_file', type=file_type, help='A file containing the job specification in JSON (formatted to match the respective REST API body). If this parameter is specified, all \'Job Arguments\' are ignored.', validator=validate_json_file, completer=FilesCompleter())
        c.argument('template', type=file_type, arg_group='Batch Extensions', help='A Batch job JSON template file. If this parameter is specified, all other parameters are ignored.', completer=FilesCompleter())
        c.argument('parameters', type=file_type, arg_group='Batch Extensions', help='Parameter values for a Batch job JSON template file. Can only be used with --template.', completer=FilesCompleter())
        c.argument('metadata', arg_group='Job', nargs='+', type=metadata_item_format)
        c.argument('uses_task_dependencies', arg_group='Job', action='store_true', help='The flag that determines if this job will use tasks with dependencies. True if flag present.')
        c.argument('pool_id', arg_group='Job: Pool Info', help='The id of an existing pool. All the tasks of the job will run on the specified pool.')
        c.argument('job_max_task_retry_count', arg_group='Job: Constraints', help='The maximum number of times each task may be retried. The Batch service retries a task if its exit code is nonzero. Note that this value specifically controls the number of retries. The Batch service will try each task once, and may then retry up to this limit. For example, if the maximum retry count is 3, Batch tries a task up to 4 times (one initial try and 3 retries). If the maximum retry count is 0, the Batch service does not retry tasks. If the maximum retry count is -1, the Batch service retries tasks without limit. The default value is 0 (no retries).')
        c.argument('job_max_wall_clock_time', arg_group='Job: Constraints', help='The maximum elapsed time that the job may run, measured from the time the job is created. If the job does not complete within the time limit, the Batch service terminates it and any tasks that are still running. In this case, the termination reason will be MaxWallClockTimeExpiry. If this property is not specified, there is no time limit on how long the job may run. Expected format is an ISO-8601 duration.')
        c.argument('job_manager_task_command_line', arg_group='Job: Job Manager Task', help='The command line of the Job Manager task. The command line does not run under a shell, and therefore cannot take advantage of shell features such as environment variable expansion. If you want to take advantage of such features, you should invoke the shell in the command line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c MyCommand" in Linux.')
        c.argument('job_manager_task_environment_settings', arg_group='Job: Job Manager Task', type=environment_setting_format, help='A list of environment variable settings for the Job Manager task. Space separated values in \'key=value\' format.')
        c.argument('job_manager_task_resource_files', arg_group='Job: Job Manager Task', type=resource_file_format, help='A list of files that the Batch service will download to the compute node before running the command line. Files listed under this element are located in the task\'s working directory. Space separated resource references in filename=httpurl format.')
        c.argument('job_manager_task_id', arg_group='Job: Job Manager Task', help='A string that uniquely identifies the Job Manager task within the job. The id can contain any combination of alphanumeric characters including hyphens and underscores and cannot contain more than 64 characters.')
        c.argument('required_slots', arg_group='Job: Job Manager Task', help='The number of scheduling slots that the Task requires to run. The default is 1. A Task can only be scheduled to run on a compute node if the node has enough free scheduling slots available. For multi-instance Tasks, this property is not supported and must not be specified.')
        c.argument('allow_task_preemption', arg_group='Job')
        c.argument('max_parallel_tasks', arg_group='Job')
        c.argument('id', arg_group='Job')
        c.argument('priority', arg_group='Job')
        
        

    

    with self.argument_context('batch file upload') as c:
        c.argument('local_path', type=file_type, help='Path to a local file or directory to be uploaded - can include wildcard patterns.')
        c.argument('file_group', help='Name of a file group under which the files will be stored.')
        c.argument('remote_path', help='Group subdirectory under which files will be uploaded.')
        c.argument('flatten', action='store_true', help='If set, will not retain local directory structure in storage.')

    with self.argument_context('batch file download') as c:
        c.argument('local_path', type=file_type, help='Path to a local file or directory to be stored the download files.')
        c.argument('file_group', help='Name of a file group from which the files will be downloaded.')
        c.argument('remote_path', help='The subdirectory under which files exist remotely.')
        c.argument('overwrite', action='store_true', help='If set, an existing file in the local path will be overwritten.')

    for item in ['batch pool create', 'batch job create', 'batch file upload', 'batch file download']:
        with self.argument_context(item) as c:
            c.extra('account_name', arg_group='Batch Account', validator=validate_client_parameters,
                    help='The Batch account name. Alternatively, set by environment variable: AZURE_BATCH_ACCOUNT')
            c.extra('account_key', arg_group='Batch Account',
                    help='The Batch account key. Alternatively, set by environment variable: AZURE_BATCH_ACCESS_KEY')
            c.extra('account_endpoint', arg_group='Batch Account',
                    help='Batch service endpoint. Alternatively, set by environment variable: AZURE_BATCH_ENDPOINT')
            c.extra('resource_group', arg_group='Batch Account',
                    help='The resource group of the Batch account')
