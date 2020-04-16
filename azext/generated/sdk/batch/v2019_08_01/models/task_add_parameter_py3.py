# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class TaskAddParameter(Model):
    """An Azure Batch Task to add.

    Batch will retry Tasks when a recovery operation is triggered on a Node.
    Examples of recovery operations include (but are not limited to) when an
    unhealthy Node is rebooted or a Compute Node disappeared due to host
    failure. Retries due to recovery operations are independent of and are not
    counted against the maxTaskRetryCount. Even if the maxTaskRetryCount is 0,
    an internal retry due to a recovery operation may occur. Because of this,
    all Tasks should be idempotent. This means Tasks need to tolerate being
    interrupted and restarted without causing any corruption or duplicate data.
    The best practice for long running Tasks is to use some form of
    checkpointing.

    All required parameters must be populated in order to send to Azure.

    :param id: Required. A string that uniquely identifies the Task within the
     Job. The ID can contain any combination of alphanumeric characters
     including hyphens and underscores, and cannot contain more than 64
     characters. The ID is case-preserving and case-insensitive (that is, you
     may not have two IDs within a Job that differ only by case).
    :type id: str
    :param display_name: A display name for the Task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: Required. The command line of the Task. For
     multi-instance Tasks, the command line is executed as the primary Task,
     after the primary Task and all subtasks have finished executing the
     coordination command line. The command line does not run under a shell,
     and therefore cannot take advantage of shell features such as environment
     variable expansion. If you want to take advantage of such features, you
     should invoke the shell in the command line, for example using "cmd /c
     MyCommand" in Windows or "/bin/sh -c MyCommand" in Linux. If the command
     line refers to file paths, it should use a relative path (relative to the
     Task working directory), or use the Batch provided environment variable
     (https://docs.microsoft.com/en-us/azure/batch/batch-compute-node-environment-variables).
    :type command_line: str
    :param container_settings: The settings for the container under which the
     Task runs. If the Pool that will run this Task has containerConfiguration
     set, this must be set as well. If the Pool that will run this Task doesn't
     have containerConfiguration set, this must not be set. When this is
     specified, all directories recursively below the AZ_BATCH_NODE_ROOT_DIR
     (the root of Azure Batch directories on the node) are mapped into the
     container, all Task environment variables are mapped into the container,
     and the Task command line is executed in the container. Files produced in
     the container outside of AZ_BATCH_NODE_ROOT_DIR might not be reflected to
     the host disk, meaning that Batch file APIs will not be able to access
     those files.
    :type container_settings: ~azure.batch.models.TaskContainerSettings
    :param exit_conditions: How the Batch service should respond when the Task
     completes.
    :type exit_conditions: ~azure.batch.models.ExitConditions
    :param resource_files: A list of files that the Batch service will
     download to the Compute Node before running the command line. For
     multi-instance Tasks, the resource files will only be downloaded to the
     Compute Node on which the primary Task is executed. There is a maximum
     size for the list of resource files.  When the max size is exceeded, the
     request will fail and the response error code will be
     RequestEntityTooLarge. If this occurs, the collection of ResourceFiles
     must be reduced in size. This can be achieved using .zip files,
     Application Packages, or Docker Containers.
    :type resource_files: list[~azure.batch.models.ResourceFile]
    :param output_files: A list of files that the Batch service will upload
     from the Compute Node after running the command line. For multi-instance
     Tasks, the files will only be uploaded from the Compute Node on which the
     primary Task is executed.
    :type output_files: list[~azure.batch.models.OutputFile]
    :param environment_settings: A list of environment variable settings for
     the Task.
    :type environment_settings: list[~azure.batch.models.EnvironmentSetting]
    :param affinity_info: A locality hint that can be used by the Batch
     service to select a Compute Node on which to start the new Task.
    :type affinity_info: ~azure.batch.models.AffinityInformation
    :param constraints: The execution constraints that apply to this Task. If
     you do not specify constraints, the maxTaskRetryCount is the
     maxTaskRetryCount specified for the Job, the maxWallClockTime is infinite,
     and the retentionTime is 7 days.
    :type constraints: ~azure.batch.models.TaskConstraints
    :param user_identity: The user identity under which the Task runs. If
     omitted, the Task runs as a non-administrative user unique to the Task.
    :type user_identity: ~azure.batch.models.UserIdentity
    :param multi_instance_settings: An object that indicates that the Task is
     a multi-instance Task, and contains information about how to run the
     multi-instance Task.
    :type multi_instance_settings: ~azure.batch.models.MultiInstanceSettings
    :param depends_on: The Tasks that this Task depends on. This Task will not
     be scheduled until all Tasks that it depends on have completed
     successfully. If any of those Tasks fail and exhaust their retry counts,
     this Task will never be scheduled. If the Job does not have
     usesTaskDependencies set to true, and this element is present, the request
     fails with error code TaskDependenciesNotSpecifiedOnJob.
    :type depends_on: ~azure.batch.models.TaskDependencies
    :param application_package_references: A list of Packages that the Batch
     service will deploy to the Compute Node before running the command line.
     Application packages are downloaded and deployed to a shared directory,
     not the Task working directory. Therefore, if a referenced package is
     already on the Node, and is up to date, then it is not re-downloaded; the
     existing copy on the Compute Node is used. If a referenced Package cannot
     be installed, for example because the package has been deleted or because
     download failed, the Task fails.
    :type application_package_references:
     list[~azure.batch.models.ApplicationPackageReference]
    :param authentication_token_settings: The settings for an authentication
     token that the Task can use to perform Batch service operations. If this
     property is set, the Batch service provides the Task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an Account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the Task can carry out using the token depend on the settings. For
     example, a Task can request Job permissions in order to add other Tasks to
     the Job, or check the status of the Job or of other Tasks under the Job.
    :type authentication_token_settings:
     ~azure.batch.models.AuthenticationTokenSettings
    """

    _validation = {
        'id': {'required': True},
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ResourceFile]'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'multi_instance_settings': {'key': 'multiInstanceSettings', 'type': 'MultiInstanceSettings'},
        'depends_on': {'key': 'dependsOn', 'type': 'TaskDependencies'},
        'application_package_references': {'key': 'applicationPackageReferences', 'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings', 'type': 'AuthenticationTokenSettings'},
    }

    def __init__(self, *, id: str, command_line: str, display_name: str=None, container_settings=None, exit_conditions=None, resource_files=None, output_files=None, environment_settings=None, affinity_info=None, constraints=None, user_identity=None, multi_instance_settings=None, depends_on=None, application_package_references=None, authentication_token_settings=None, **kwargs) -> None:
        super(TaskAddParameter, self).__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.command_line = command_line
        self.container_settings = container_settings
        self.exit_conditions = exit_conditions
        self.resource_files = resource_files
        self.output_files = output_files
        self.environment_settings = environment_settings
        self.affinity_info = affinity_info
        self.constraints = constraints
        self.user_identity = user_identity
        self.multi_instance_settings = multi_instance_settings
        self.depends_on = depends_on
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
