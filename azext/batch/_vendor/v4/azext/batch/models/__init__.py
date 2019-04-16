# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=wildcard-import,unused-import,unused-wildcard-import

# Not ideal syntax - but savaes us having to check and repopulate this
# list every time the SDK is regenerated.
from ....azure.batch.models import *

try:
    from .extended_task_parameter_py3 import ExtendedTaskParameter
    from .extended_job_parameter_py3 import ExtendedJobParameter
    from .extended_pool_parameter_py3 import ExtendedPoolParameter
    from .extended_pool_specification_py3 import ExtendedPoolSpecification
    from .auto_pool_specification_py3 import AutoPoolSpecification
    from .output_file_py3 import OutputFile
    from .extended_output_file_destination_py3 import ExtendedOutputFileDestination
    from .output_file_auto_storage_destination_py3 import OutputFileAutoStorageDestination
    from .extended_resource_file_py3 import ExtendedResourceFile
    from .multi_instance_settings_py3 import MultiInstanceSettings
    from .file_source_py3 import FileSource
    from .task_factory_base_py3 import TaskFactoryBase
    from .task_collection_task_factory_py3 import TaskCollectionTaskFactory
    from .parametric_sweep_task_factory_py3 import ParametricSweepTaskFactory
    from .file_collection_task_factory_py3 import FileCollectionTaskFactory
    from .parameter_set_py3 import ParameterSet
    from .repeat_task_py3 import RepeatTask
    from .package_reference_base_py3 import PackageReferenceBase
    from .chocolatey_package_reference_py3 import ChocolateyPackageReference
    from .yum_package_reference_py3 import YumPackageReference
    from .apt_package_reference_py3 import AptPackageReference
    from .application_template_info_py3 import ApplicationTemplateInfo
    from .merge_task_py3 import MergeTask
    from .job_preparation_task_py3 import JobPreparationTask
    from .job_release_task_py3 import JobReleaseTask
    from .job_manager_task_py3 import JobManagerTask
    from .start_task_py3 import StartTask
    from .application_template_py3 import ApplicationTemplate
    from .job_template_py3 import JobTemplate
    from .pool_template_py3 import PoolTemplate
except (SyntaxError, ImportError):
    from .extended_task_parameter import ExtendedTaskParameter
    from .extended_job_parameter import ExtendedJobParameter
    from .extended_pool_parameter import ExtendedPoolParameter
    from .extended_pool_specification import ExtendedPoolSpecification
    from .auto_pool_specification import AutoPoolSpecification
    from .output_file import OutputFile
    from .extended_output_file_destination import ExtendedOutputFileDestination
    from .output_file_auto_storage_destination import OutputFileAutoStorageDestination
    from .extended_resource_file import ExtendedResourceFile
    from .multi_instance_settings import MultiInstanceSettings
    from .file_source import FileSource
    from .task_factory_base import TaskFactoryBase
    from .task_collection_task_factory import TaskCollectionTaskFactory
    from .parametric_sweep_task_factory import ParametricSweepTaskFactory
    from .file_collection_task_factory import FileCollectionTaskFactory
    from .parameter_set import ParameterSet
    from .repeat_task import RepeatTask
    from .package_reference_base import PackageReferenceBase
    from .chocolatey_package_reference import ChocolateyPackageReference
    from .yum_package_reference import YumPackageReference
    from .apt_package_reference import AptPackageReference
    from .application_template_info import ApplicationTemplateInfo
    from .merge_task import MergeTask
    from .job_preparation_task import JobPreparationTask
    from .job_release_task import JobReleaseTask
    from .job_manager_task import JobManagerTask
    from .start_task import StartTask
    from .application_template import ApplicationTemplate
    from .job_template import JobTemplate
    from .pool_template import PoolTemplate

from .constants import (
    PROPS_RESERVED_FOR_JOBS,
    PROPS_PERMITTED_ON_TEMPLATES)

__all__ = [
    'ExtendedTaskParameter',
    'ExtendedJobParameter',
    'ExtendedPoolParameter',
    'ExtendedPoolSpecification',
    'AutoPoolSpecification',
    'OutputFile',
    'ExtendedOutputFileDestination',
    'OutputFileAutoStorageDestination',
    'ExtendedResourceFile',
    'MultiInstanceSettings',
    'FileSource',
    'TaskFactoryBase',
    'TaskCollectionTaskFactory',
    'ParametricSweepTaskFactory',
    'FileCollectionTaskFactory',
    'ParameterSet',
    'RepeatTask',
    'PackageReferenceBase',
    'ChocolateyPackageReference',
    'YumPackageReference',
    'AptPackageReference',
    'ApplicationTemplateInfo',
    'MergeTask',
    'JobPreparationTask',
    'JobReleaseTask',
    'JobManagerTask',
    'StartTask',
    'ApplicationTemplate',
    'JobTemplate',
    'PoolTemplate',
]
