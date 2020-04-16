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


class StartTask(Model):
    """A Task which is run when a Node joins a Pool in the Azure Batch service, or
    when the Compute Node is rebooted or reimaged.

    Batch will retry Tasks when a recovery operation is triggered on a Node.
    Examples of recovery operations include (but are not limited to) when an
    unhealthy Node is rebooted or a Compute Node disappeared due to host
    failure. Retries due to recovery operations are independent of and are not
    counted against the maxTaskRetryCount. Even if the maxTaskRetryCount is 0,
    an internal retry due to a recovery operation may occur. Because of this,
    all Tasks should be idempotent. This means Tasks need to tolerate being
    interrupted and restarted without causing any corruption or duplicate data.
    The best practice for long running Tasks is to use some form of
    checkpointing. In some cases the StartTask may be re-run even though the
    Compute Node was not rebooted. Special care should be taken to avoid
    StartTasks which create breakaway process or install/launch services from
    the StartTask working directory, as this will block Batch from being able
    to re-run the StartTask.

    All required parameters must be populated in order to send to Azure.

    :param command_line: Required. The command line of the StartTask. The
     command line does not run under a shell, and therefore cannot take
     advantage of shell features such as environment variable expansion. If you
     want to take advantage of such features, you should invoke the shell in
     the command line, for example using "cmd /c MyCommand" in Windows or
     "/bin/sh -c MyCommand" in Linux. If the command line refers to file paths,
     it should use a relative path (relative to the Task working directory), or
     use the Batch provided environment variable
     (https://docs.microsoft.com/en-us/azure/batch/batch-compute-node-environment-variables).
    :type command_line: str
    :param container_settings: The settings for the container under which the
     StartTask runs. When this is specified, all directories recursively below
     the AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch directories on the
     node) are mapped into the container, all Task environment variables are
     mapped into the container, and the Task command line is executed in the
     container. Files produced in the container outside of
     AZ_BATCH_NODE_ROOT_DIR might not be reflected to the host disk, meaning
     that Batch file APIs will not be able to access those files.
    :type container_settings: ~azure.batch.models.TaskContainerSettings
    :param resource_files: A list of files that the Batch service will
     download to the Compute Node before running the command line.  There is a
     maximum size for the list of resource files. When the max size is
     exceeded, the request will fail and the response error code will be
     RequestEntityTooLarge. If this occurs, the collection of ResourceFiles
     must be reduced in size. This can be achieved using .zip files,
     Application Packages, or Docker Containers. Files listed under this
     element are located in the Task's working directory.
    :type resource_files: list[~azure.batch.models.ResourceFile]
    :param environment_settings: A list of environment variable settings for
     the StartTask.
    :type environment_settings: list[~azure.batch.models.EnvironmentSetting]
    :param user_identity: The user identity under which the StartTask runs. If
     omitted, the Task runs as a non-administrative user unique to the Task.
    :type user_identity: ~azure.batch.models.UserIdentity
    :param max_task_retry_count: The maximum number of times the Task may be
     retried. The Batch service retries a Task if its exit code is nonzero.
     Note that this value specifically controls the number of retries. The
     Batch service will try the Task once, and may then retry up to this limit.
     For example, if the maximum retry count is 3, Batch tries the Task up to 4
     times (one initial try and 3 retries). If the maximum retry count is 0,
     the Batch service does not retry the Task. If the maximum retry count is
     -1, the Batch service retries the Task without limit.
    :type max_task_retry_count: int
    :param wait_for_success: Whether the Batch service should wait for the
     StartTask to complete successfully (that is, to exit with exit code 0)
     before scheduling any Tasks on the Compute Node. If true and the StartTask
     fails on a Node, the Batch service retries the StartTask up to its maximum
     retry count (maxTaskRetryCount). If the Task has still not completed
     successfully after all retries, then the Batch service marks the Node
     unusable, and will not schedule Tasks to it. This condition can be
     detected via the Compute Node state and failure info details. If false,
     the Batch service will not wait for the StartTask to complete. In this
     case, other Tasks can start executing on the Compute Node while the
     StartTask is still running; and even if the StartTask fails, new Tasks
     will continue to be scheduled on the Compute Node. The default is true.
    :type wait_for_success: bool
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'max_task_retry_count': {'key': 'maxTaskRetryCount', 'type': 'int'},
        'wait_for_success': {'key': 'waitForSuccess', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(StartTask, self).__init__(**kwargs)
        self.command_line = kwargs.get('command_line', None)
        self.container_settings = kwargs.get('container_settings', None)
        self.resource_files = kwargs.get('resource_files', None)
        self.environment_settings = kwargs.get('environment_settings', None)
        self.user_identity = kwargs.get('user_identity', None)
        self.max_task_retry_count = kwargs.get('max_task_retry_count', None)
        self.wait_for_success = kwargs.get('wait_for_success', None)
