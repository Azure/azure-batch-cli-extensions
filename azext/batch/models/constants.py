# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from enum import Enum

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


# Ensure the first member of this array is the official REST Version
class SupportedRestApi(Enum):
    Aug2018 = ["2018-08-01.7.0", "2018-08-01"]
    Dec2018 = ["2018-12-01.8.0", "2018-12-01"]
    Jun2019 = ["2019-06-01.9.0", "2019-06-01"]
    Aug2019 = ["2019-08-01.10.0", "2019-08-01", "latest"]


class SupportedTemplateApi(Enum):
    Latest = ["latest"]


SupportRestApiToSdkVersion = {
    SupportedRestApi.Aug2018: "2018_08_01",
    SupportedRestApi.Dec2018: "2018_12_01",
    SupportedRestApi.Jun2019: "2019_06_01",
    SupportedRestApi.Aug2019: "2019_08_01",
}
