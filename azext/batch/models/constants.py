# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


# These properties are reserved for application template use
# and may not be used on jobs using an application template
PROPS_RESERVED_FOR_TEMPLATES = {
    'jobManagerTask',
    'jobPreparationTask',
    'jobReleaseTask',
    #'commonEnvironmentSettings',
    'usesTaskDependencies',
    'onAllTasksComplete',
    'onTaskFailure',
    'taskFactory'}


PROPS_PERMITTED_ON_TEMPLATES = PROPS_RESERVED_FOR_TEMPLATES.union({
    'templateMetadata',
    'parameters',
    'metadata'})


ATTRS_RESERVED_FOR_TEMPLATES = {
    'job_manager_task',
    'job_preparation_task',
    'job_release_task',
    #'common_environment_settings',
    'uses_task_dependencies',
    'on_all_tasks_complete',
    'on_task_failure',
    'task_factory'}


# These properties are reserved for job use
# and may not be used on an application template
PROPS_RESERVED_FOR_JOBS = {
    'id',
    'displayName',
    'priority',
    'constraints',
    'poolInfo',
    'applicationTemplateInfo'}


# Properties on a repeatTask object that should be
# applied to each expanded task.
PROPS_ON_REPEAT_TASK = {
    'displayName',
    'containerSettings',
    'resourceFiles',
    'environmentSettings',
    'constraints',
    'userIdentity',
    'exitConditions',
    'clientExtensions',
    'outputFiles',
    'packageReferences'}


PROPS_ON_COLLECTION_TASK = PROPS_ON_REPEAT_TASK.union({
    'multiInstanceSettings',
    'dependsOn'})
