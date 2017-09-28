# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.serialization import Model


class RepeatTask(Model):
    """An Azure Batch task template to repeat.

    :param display_name: A display name for the task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: The command line of the task.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     task runs. If the pool that will run this task has containerConfiguration
     set, this must be set as well. If the pool that will run this task doesn't
     have containerConfiguration set, this must not be set. When this is
     specified, all directories recursively below the AZ_BATCH_NODE_ROOT_DIR
     (the root of Azure Batch directories on the node) are mapped into the
     container, all task environment variables are mapped into the container,
     and the task command line is executed in the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param exit_conditions: How the Batch service should respond when the task
     completes.
    :type exit_conditions: :class:`ExitConditions
     <azure.batch.models.ExitConditions>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azure.batch_extensions.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param affinity_info: A locality hint that can be used by the Batch
     service to select a compute node on which to start the new task.
    :type affinity_info: :class:`AffinityInformation
     <azure.batch.models.AffinityInformation>`
    :param constraints: The execution constraints that apply to this task. If
     you do not specify constraints, the maxTaskRetryCount is the
     maxTaskRetryCount specified for the job, and the maxWallClockTime and
     retentionTime are infinite.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param user_identity: The user identity under which the task runs. If
     omitted, the task runs as a non-administrative user unique to the task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param application_package_references: A list of application packages that
     the Batch service will deploy to the compute node before running the
     command line.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param authentication_token_settings: The settings for an authentication
     token that the task can use to perform Batch service operations. If this
     property is set, the Batch service provides the task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the task can carry out using the token depend on the settings. For
     example, a task can request job permissions in order to add other tasks to
     the job, or check the status of the job or of other tasks under the job.
    :type authentication_token_settings: :class:`AuthenticationTokenSettings
     <azure.batch.models.AuthenticationTokenSettings>`
    :param output_files: A list of output file references to up persisted once
     the task has completed.
    :type output_files: list of :class:`OutputFile
     <azure.batch_extensions.models.OutputFile>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azure.batch_extensions.models.PackageReferenceBase>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'}
    }

    def __init__(self, command_line, display_name=None, container_settings=None, exit_conditions=None,
                 resource_files=None, environment_settings=None, affinity_info=None, constraints=None,
                 user_identity=None, application_package_references=None, authentication_token_settings=None,
                 output_files=None, package_references=None):
        self.display_name = display_name
        self.command_line = command_line
        self.container_settings = container_settings
        self.exit_conditions = exit_conditions
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.affinity_info = affinity_info
        self.constraints = constraints
        self.user_identity = user_identity
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
        self.output_files = output_files
        self.package_references = package_references
