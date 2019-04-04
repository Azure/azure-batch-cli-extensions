# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=redefined-builtin

from msrest.serialization import Model


class JobReleaseTask(Model):
    """A Job Release task to run on job completion on any compute node where the
    job has run.

    The Job Release task runs when the job ends, because of one of the
    following: The user calls the Terminate Job API, or the Delete Job API
    while the job is still active, the job's maximum wall clock time constraint
    is reached, and the job is still active, or the job's Job Manager task
    completed, and the job is configured to terminate when the Job Manager
    completes. The Job Release task runs on each compute node where tasks of
    the job have run and the Job Preparation task ran and completed. If you
    reimage a compute node after it has run the Job Preparation task, and the
    job ends without any further tasks of the job running on that compute node
    (and hence the Job Preparation task does not re-run), then the Job Release
    task does not run on that node. If a compute node reboots while the Job
    Release task is still running, the Job Release task runs again when the
    compute node starts up. The job is not marked as complete until all Job
    Release tasks have completed. The Job Release task runs in the background.
    It does not occupy a scheduling slot; that is, it does not count towards
    the maxTasksPerNode limit specified on the pool.

    :param id: A string that uniquely identifies the Job Release task within
     the job. The ID can contain any combination of alphanumeric characters
     including hyphens and underscores and cannot contain more than 64
     characters. If you do not specify this property, the Batch service assigns
     a default value of 'jobrelease'. No other task in the job can have the
     same ID as the Job Release task. If you try to submit a task with the same
     ID, the Batch service rejects the request with error code
     TaskIdSameAsJobReleaseTask; if you are calling the REST API directly, the
     HTTP status code is 409 (Conflict).
    :type id: str
    :param command_line: The command line of the Job Release task. The command
     line does not run under a shell, and therefore cannot take advantage of
     shell features such as environment variable expansion. If you want to take
     advantage of such features, you should invoke the shell in the command
     line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c
     MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     Job Release task runs. When this is specified, all directories recursively
     below the AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch directories on
     the node) are mapped into the container, all task environment variables
     are mapped into the container, and the task command line is executed in
     the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. Files listed
     under this element are located in the task's working directory.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the Job Release task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param max_wall_clock_time: The maximum elapsed time that the Job Release
     task may run on a given compute node, measured from the time the task
     starts. If the task does not complete within the time limit, the Batch
     service terminates it. The default value is 15 minutes. You may not
     specify a timeout longer than 15 minutes. If you do, the Batch service
     rejects it with an error; if you are calling the REST API directly, the
     HTTP status code is 400 (Bad Request).
    :type max_wall_clock_time: timedelta
    :param retention_time: The minimum time to retain the task directory for
     the Job Release task on the compute node. After this time, the Batch
     service may delete the task directory and all its contents. The default is
     infinite, i.e. the task directory will be retained until the compute node
     is removed or reimaged.
    :type retention_time: timedelta
    :param user_identity: The user identity under which the Job Release task
     runs. If omitted, the task runs as a non-administrative user unique to the
     task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'max_wall_clock_time': {'key': 'maxWallClockTime', 'type': 'duration'},
        'retention_time': {'key': 'retentionTime', 'type': 'duration'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
    }

    def __init__(self, **kwargs):
        super(JobReleaseTask, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.command_line = kwargs.get('command_line', None)
        self.container_settings = kwargs.get('container_settings', None)
        self.resource_files = kwargs.get('resource_files', None)
        self.environment_settings = kwargs.get('environment_settings', None)
        self.max_wall_clock_time = kwargs.get('max_wall_clock_time', None)
        self.retention_time = kwargs.get('retention_time', None)
        self.user_identity = kwargs.get('user_identity', None)
