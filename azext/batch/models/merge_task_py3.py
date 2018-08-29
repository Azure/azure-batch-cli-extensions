# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=redefined-builtin

from msrest.serialization import Model


class MergeTask(Model):
    """An Azure Batch task template to repeat.

    :param str id: The ID of the merge task.
    :param display_name: A display name for the task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: The command line of the task. For multi-instance
     tasks, the command line is executed as the primary task, after the primary
     task and all subtasks have finished executing the coordination command
     line. The command line does not run under a shell, and therefore cannot
     take advantage of shell features such as environment variable expansion.
     If you want to take advantage of such features, you should invoke the
     shell in the command line, for example using "cmd /c MyCommand" in Windows
     or "/bin/sh -c MyCommand" in Linux.
    :type command_line: str
    :param exit_conditions: How the Batch service should respond when the task
     completes.
    :type exit_conditions: :class:`ExitConditions
     <azure.batch.models.ExitConditions>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. For
     multi-instance tasks, the resource files will only be downloaded to the
     compute node on which the primary task is executed.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
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
    :param depends_on: The tasks that this task depends on. This task will not
     be scheduled until all tasks that it depends on have completed
     successfully. If any of those tasks fail and exhaust their retry counts,
     this task will never be scheduled. If the job does not have
     usesTaskDependencies set to true, and this element is present, the request
     fails with error code TaskDependenciesNotSpecifiedOnJob.
    :type depends_on: :class:`TaskDependencies
     <azure.batch.models.TaskDependencies>`
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
     <azext.batch.models.OutputFile>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'depends_on': {'key': 'dependsOn', 'type': 'TaskDependencies'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'},
    }

    def __init__(self, *, command_line: str, id: str=None, display_name: str=None, exit_conditions=None,
                 resource_files=None, environment_settings=None, affinity_info=None, constraints=None,
                 user_identity=None, depends_on=None, application_package_references=None,
                 authentication_token_settings=None, output_files=None, package_references=None, **kwargs):
        self.id = id
        self.display_name = display_name
        self.command_line = command_line
        self.exit_conditions = exit_conditions
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.affinity_info = affinity_info
        self.constraints = constraints
        self.user_identity = user_identity
        self.depends_on = depends_on
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
        self.output_files = output_files
        self.package_references = package_references
