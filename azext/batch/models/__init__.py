# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=wildcard-import,unused-import,unused-wildcard-import

# Not ideal syntax - but saves us having to check and repopulate this
# list every time the SDK is regenerated.
from ...generated.sdk.batch.v2019_08_01.models import *
try:
    from ._models_py3 import ExtendedTaskParameter
    from ._models_py3 import ExtendedJobParameter
    from ._models_py3 import ExtendedPoolParameter
    from ._models_py3 import ExtendedPoolSpecification
    from ._models_py3 import AutoPoolSpecification
    from ._models_py3 import OutputFile
    from ._models_py3 import ExtendedOutputFileDestination
    from ._models_py3 import OutputFileAutoStorageDestination
    from ._models_py3 import ExtendedResourceFile
    from ._models_py3 import MultiInstanceSettings
    from ._models_py3 import FileSource
    from ._models_py3 import TaskFactoryBase
    from ._models_py3 import TaskCollectionTaskFactory
    from ._models_py3 import ParametricSweepTaskFactory
    from ._models_py3 import FileCollectionTaskFactory
    from ._models_py3 import ParameterSet
    from ._models_py3 import RepeatTask
    from ._models_py3 import PackageReferenceBase
    from ._models_py3 import ChocolateyPackageReference
    from ._models_py3 import YumPackageReference
    from ._models_py3 import AptPackageReference
    from ._models_py3 import ApplicationTemplateInfo
    from ._models_py3 import MergeTask
    from ._models_py3 import JobPreparationTask
    from ._models_py3 import JobReleaseTask
    from ._models_py3 import JobManagerTask
    from ._models_py3 import StartTask
    from ._models_py3 import ApplicationTemplate
    from ._models_py3 import JobTemplate
    from ._models_py3 import PoolTemplate
except (SyntaxError, ImportError):
    from ._models import ExtendedTaskParameter
    from ._models import ExtendedJobParameter
    from ._models import ExtendedPoolParameter
    from ._models import ExtendedPoolSpecification
    from ._models import AutoPoolSpecification
    from ._models import OutputFile
    from ._models import ExtendedOutputFileDestination
    from ._models import OutputFileAutoStorageDestination
    from ._models import ExtendedResourceFile
    from ._models import MultiInstanceSettings
    from ._models import FileSource
    from ._models import TaskFactoryBase
    from ._models import TaskCollectionTaskFactory
    from ._models import ParametricSweepTaskFactory
    from ._models import FileCollectionTaskFactory
    from ._models import ParameterSet
    from ._models import RepeatTask
    from ._models import PackageReferenceBase
    from ._models import ChocolateyPackageReference
    from ._models import YumPackageReference
    from ._models import AptPackageReference
    from ._models import ApplicationTemplateInfo
    from ._models import MergeTask
    from ._models import JobPreparationTask
    from ._models import JobReleaseTask
    from ._models import JobManagerTask
    from ._models import StartTask
    from ._models import ApplicationTemplate
    from ._models import JobTemplate
    from ._models import PoolTemplate

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
