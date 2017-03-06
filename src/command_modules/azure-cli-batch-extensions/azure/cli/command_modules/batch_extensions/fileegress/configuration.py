#
# Copyright (c) Microsoft and contributors.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#

import enum
import json


class SpecificationEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return o.value
        except AttributeError:
            return o.__dict__


class Specification(object):
    def __init__(self, output_files=None):
        # type: (List[OutputFile]) -> None
        self.output_files = \
            output_files if output_files else []  # type: List[OutputFile]

    @staticmethod
    def from_dict(d):
        # type: (Dict[str, str]) -> Specification
        result = [OutputFile.from_dict(item) for item in d['outputFiles']]
        spec = Specification(result)
        return spec


class BlobContainerDestination(object):
    def __init__(self, container_sas, path=None):
        # type: (str, str) -> None
        self.path = path  # type: str
        self.container_sas = container_sas  # type: str

    @staticmethod
    def from_dict(d):
        # type: (Dict[str, str]) -> BlobContainerDestination
        # required arguments
        try:
            container_sas = d.pop('containerSas')
        except KeyError as e:
            raise ValueError('Missing required {}'.format(e.args[0]))

        # optional arguments
        path = d.pop('path', None)

        if len(d) > 0:
            raise ValueError('unexpected keys {}'.format(list(d.keys())))

        result = BlobContainerDestination(container_sas, path)
        return result


class OutputFileDestination(object):
    def __init__(self, container):
        # type: (BlobContainerDestination) -> None
        self.container = container  # type: BlobContainerDestination

    @staticmethod
    def from_dict(d):
        # type: (Dict[str, str]) -> OutputFileDestination
        # required arguments
        try:
            container = d.pop('container')
        except KeyError as e:
            raise ValueError('Missing required {}'.format(e.args[0]))

        # optional arguments

        if len(d) > 0:
            raise ValueError('unexpected keys {}'.format(list(d.keys())))

        container = BlobContainerDestination.from_dict(container)
        result = OutputFileDestination(container)
        return result


class TaskStatus(enum.Enum):
    TaskFailure = 'TaskFailure'
    TaskSuccess = 'TaskSuccess'
    TaskCompletion = 'TaskCompletion'


class OutputFileUploadDetails(object):
    def __init__(self, task_status):
        # type: (TaskStatus) -> None
        self.task_status = task_status  # type: TaskStatus

    @staticmethod
    def from_dict(d):
        # type: (Dict[str, str]) -> OutputFileUploadDetails
        # required arguments
        try:
            task_status = d.pop('taskStatus')
        except KeyError as e:
            raise ValueError('Missing required {}'.format(e.args[0]))

        if len(d) > 0:
            raise ValueError('unexpected keys {}'.format(list(d.keys())))

        # deserialize task_status into an enum
        task_status = TaskStatus(task_status)

        return OutputFileUploadDetails(task_status)


class OutputFile(object):
    def __init__(self, file_pattern, destination, upload_details):
        # type: (str, OutputFileDestination, OutputFileUploadDetails) -> None
        self.file_pattern = file_pattern  # type: str
        self.destination = destination  # type: OutputFileDestination
        self.upload_details = upload_details  # type: OutputFileUploadDetails

    @staticmethod
    def from_dict(d):
        # type: (Dict[str, str]) -> OutputFile
        # required arguments
        try:
            file_pattern = d.pop('filePattern')
            upload_details = d.pop('uploadDetails')
            destination = d.pop('destination')
        except KeyError as e:
            raise ValueError('Missing required {}'.format(e.args[0]))

        # optional arguments

        if len(d) > 0:
            raise ValueError('unexpected keys {}'.format(list(d.keys())))

        destination = OutputFileDestination.from_dict(destination)
        upload_details = OutputFileUploadDetails.from_dict(upload_details)

        result = OutputFile(file_pattern, destination, upload_details)
        return result


# Classes used for output
class ErrorCode(enum.Enum):
    InternalError = 'InternalError'
    AuthenticationFailed = 'AuthenticationFailed'
    ContainerNotFound = 'ContainerNotFound'
    Conflict = 'Conflict'
    UnknownError = 'UnknownError'
    PreconditionFailed = 'PreconditionFailed'


class ErrorSpecification(object):
    def __init__(self, code, user_error, pattern, file):
        # type: (ErrorCode, bool, Optional[str], Optional[str]) -> None
        self.code = code
        self.user_error = user_error
        self.pattern = pattern
        self.file = file
