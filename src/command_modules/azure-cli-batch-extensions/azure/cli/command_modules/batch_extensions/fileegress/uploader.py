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

# stdlib imports
from __future__ import print_function
import logging
import logging.handlers
import os
import sys
import traceback
import multiprocessing
try:
    import pathlib
except:
    import pathlib2 as pathlib
try:
    import urllib.parse as urlparse
except:
    import urlparse
# non-stdlib imports
import azure.storage.blob
# local imports
import util
import configuration
# import typing

_NUM_STORAGE_WORKERS = max(4, multiprocessing.cpu_count())


# predefine WindowsError if we are not on windows
if 'WindowsError' not in __builtins__:
    class WindowsError(OSError):
        pass


def _extract_container_sas_token(container_sas):
    # type: str -> Tuple[str, str, str]
    """Parses a full container sas and returns the account name,
    container name, and sas token

    :param container_sas: The fully qualified container sas
    :return: A tuple of account_name, container_name, and sas_token
    """
    # TODO validate that this is actually a valid container sas
    scheme, netloc, path, query, fragment = urlparse.urlsplit(container_sas)
    path = path.strip('/')
    return netloc.split('.')[0], path, query


def _resolve_symlinks_and_relative_paths(path):
    # type: pathlib.Path -> pathlib.Path
    """Resolves symlinks and relative paths if possible

    :param path: The path
    :return: The path with symlinks and relative paths removed
    """
    try:
        path = path.resolve()
    except WindowsError:  # TODO: check for more specific error
        pass
    except OSError as e:
        if e.errno == 2:
            pass
        else:
            raise

    return path


def _extract_pathinfo(input_pattern):
    # str -> Tuple[str, str, bool, bool]:
    """Extracts details about a given pattern

    :param input_pattern: The input pattern
    :return: A 4-tuple of base_path, pattern, fullpath, recursive.
    base_path is the most-resolved path not including an actual file name
        and before any wildcards.
    pattern is input_pattern with environment variable substitution performed.
    fullpath is True if the pattern was for a single file
        (no wildcards were specified).
    recursive is True if the pattern included a '**'.
    """
    # replace any parts of the path that have env vars
    typed_path = pathlib.Path(os.path.expandvars(input_pattern))
    # prepend task working directory for relative paths
    if not typed_path.is_absolute():
        _pparts = list(typed_path.parts)
        _pparts.insert(0, os.environ['AZ_BATCH_TASK_WORKING_DIR'])
        typed_path = pathlib.Path(*_pparts)
    # get base path and check for recursive elements
    _pparts = list(typed_path.parts)
    file = []
    recursive = False
    fullpath = True
    for p in _pparts:
        if '*' in p:
            if p == '**':
                recursive = True
            fullpath = False
            break
        else:
            file.append(p)
    if fullpath:
        base_path = pathlib.Path(*file).parent
    else:
        base_path = pathlib.Path(*file)
    # attempt to resolve path to remove symlinks and relative paths
    base_path = _resolve_symlinks_and_relative_paths(base_path)
    # stamp pattern from base_path
    pattern = str(typed_path)
    base_path = str(base_path)
    if base_path == pattern:
        pattern = None
    return base_path, pattern, fullpath, recursive


def normalize_blob_name(root, file):
    # type: (str, str) -> str
    """Creates a valid Azure Storage blob name given a
    relative root and a file path.

    For example, if root='C:/users/tasks/task1' and
    file='C:/users/tasks/task1/foo/bar/test.txt', then the blob name
    would be 'foo/bar/test.txt'
    :param root: The root which the file is relative to.
    :param file: The file path
    :return: A blob name.
    """
    path = pathlib.Path(file)
    path = _resolve_symlinks_and_relative_paths(path)
    rel = str(path.relative_to(root))
    if util.on_windows():
        rel = rel.replace(os.path.sep, '/')
    return rel


def glob_files(root, pattern):
    # type: (str, str) -> Iterable
    """Creates an iterable given a file pattern.

    Note that this returns a generator not a fully resolved collection.

    :param root: The root path.
    :param pattern: The pattern to apply relative to the root path.
    :return: An iterable containing all the files which match the pattern.
    """
    root_path = pathlib.Path(root)
    pattern_path = pathlib.Path(pattern)
    local_pattern = str(pattern_path.relative_to(root))

    return root_path.glob(local_pattern)


class ResolvedFileMapping(object):
    """A file mapping containing all of the necessary details to perform a
    file upload, including both the source and the destination.
   """
    def __init__(
            self,
            base_path,  # type: str
            full_pattern,  # type: str
            is_full_path,  # type: bool
            recursive,  # type: bool
            blob_client,  # type: azure.storage.blob.BlockBlobService
            destination_container,  # type: str
            destination_path  # type: str
    ):
        self.base_path = base_path
        self.full_pattern = full_pattern
        self.is_full_path = is_full_path
        self.recursive = recursive
        self.blob_client = blob_client
        self.destination_container = destination_container
        self.destination_path = destination_path

    def calculate_destination(self, file):
        # type: (str) -> str
        """Determines the final destination of a file in the mapping.

        :param file: The file path
        :return: The full blob destination
        """

        # Handle the case where there were no wildcards (so the
        # destination IS a target blob name)
        if self.is_full_path:
            # Default to the name of the file
            if self.destination_path is None:
                destination = normalize_blob_name(self.base_path, file)
            else:
                destination = self.destination_path
        # Handle the case where there were wildcards,
        # so the destination path is a virtual directory
        else:
            # Default to the name of the file
            if self.destination_path is None:
                destination = normalize_blob_name(self.base_path, file)
            else:
                destination = '{}/{}'.format(
                    self.destination_path,
                    normalize_blob_name(self.base_path, file))

        return destination

    def __repr__(self):
        return 'Resolved mapping - base_path: {}, ' \
               'full_pattern: {}, recursive: {}, destination: {}'.format(
                    self.base_path,
                    self.full_pattern,
                    self.recursive,
                    self.destination_path)


# TODO: The C# is leaking...
class AggregateException(Exception):
    """An exception comprised entirely of other exceptions.
    """
    def __init__(self, errors):
        # type: (Tuple[str, str, List[Exception]]) -> None
        """
        Initializes an AggregateException with a collection of errors
        :param errors: A 3-tuple of file, pattern, and error
        """
        self.errors = errors  # type: List[Tuple[str, str, Exception]]

    def __repr__(self):
        result = ', '.join('file: {} from pattern: {} hit error: {}'.format(
            file,
            pattern,
            repr(error)) for file, pattern, error in self.errors)
        return result

    def __str__(self):
        return self.__repr__()


class FileUploader(object):
    def __init__(
            self,
            job_id,  # type: str
            task_id,  # type: str
    ):
        self.job_id = job_id  # type: str
        self.task_id = task_id  # type: str

        # Set up the logger
        self.logger = logging.getLogger('{}-{}'.format(
            self.job_id, self.task_id))
        self.logger.setLevel('INFO')
        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter('%(asctime)-15s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _upload_file(
            self,
            blob_client,  # type: azure.storage.blob.BlockBlobService
            container_name,  # type: str
            path,  # type: str
            blob_name  # type: str
    ):
        # type: (...) -> None
        """Uploads a single file to an Azure Storage blob

        :param blob_client: The blob client
        :param container_name: The container name
        :param path: The path of the file to upload
        :param blob_name: The blob name
        """
        self.logger.info('Uploading file: %s to container: %s blob: %s',
                         path, container_name, blob_name)
        start_time = util.datetime_utcnow()

        blob_client.create_blob_from_path(
            container_name,
            blob_name,
            path,
            max_connections=_NUM_STORAGE_WORKERS)

        end_time = util.datetime_utcnow()
        self.logger.info(
            'Upload of %s done in %s',
            path, end_time - start_time)

    @staticmethod
    def _gather_files_to_upload(
            file_info  # type: List[ResolvedFileMapping]
    ):
        # type: (...) -> List[Tuple[ResolvedFileMapping, Iterable]]
        """Gathers all of the files which should be uploaded

        :param file_info: A list of file mappings
        :return: A 2-tuple (mapping, Iterable).
        The mapping is associated with the individual Iterable of files.
        """
        files = []
        for resolved_mapping in file_info:
            matched_files = glob_files(
                resolved_mapping.base_path,
                resolved_mapping.full_pattern)
            files.append((resolved_mapping, matched_files))
        return files

    def push_file_list_to_storage(self, file_info):
        # type: (List[ResolvedFileMapping]) -> None
        """Uploads the files specified by the mapping to Azure Blob storage

        :param file_info: The file mapping
        """
        files = self._gather_files_to_upload(file_info)
        errors = []
        for resolved_mapping, file_iter in files:
            self.logger.info(
                'Uploading all files matching pattern %s',
                resolved_mapping.full_pattern)
            try:
                for file in file_iter:
                    if not file.is_file():
                        continue
                    try:
                        self._upload_file(
                            resolved_mapping.blob_client,
                            resolved_mapping.destination_container,
                            str(file),
                            resolved_mapping.calculate_destination(file))
                    except Exception as e:
                        exception_details = traceback.format_exc()
                        self.logger.info(
                            'Encountered an error while '
                            'uploading file {}. Error: {}'.format(
                                str(file), exception_details))
                        errors.append(
                            (str(file), resolved_mapping.full_pattern, e))
            except Exception as e:
                exception_details = traceback.format_exc()
                self.logger.info(
                    'Encountered an error while uploading '
                    'pattern {}. Error: {}'.format(
                        resolved_mapping.full_pattern,
                        exception_details))
                errors.append(
                    (None, resolved_mapping.full_pattern, e))

        if errors:
            raise AggregateException(errors)

    def run(self, config, task_success):
        # type: (configuration.Specification, bool) -> None
        """Runs the uploader

        :param config: The configuration
        :param task_success: True if the task succeeded,
            False if the task failed.
        None means don't upload either TaskSuccess or TaskFailure files
        """

        file_info = []
        for output_file in config.output_files:
            # Determine if this pattern should be skipped or not
            file_success = output_file.upload_details.task_status == \
                configuration.TaskStatus.TaskSuccess
            file_failure = output_file.upload_details.task_status == \
                configuration.TaskStatus.TaskFailure
            file_completion = output_file.upload_details.task_status == \
                configuration.TaskStatus.TaskCompletion

            should_upload = (
                (file_success and task_success) or
                (file_failure and not task_success) or
                file_completion)

            # Skip this pattern
            if not should_upload:
                continue

            destination = output_file.destination
            storage_account, container, sas_token = \
                _extract_container_sas_token(
                    destination.container.container_sas)

            # set up clients
            blob_client = azure.storage.blob.BlockBlobService(
                storage_account, sas_token=sas_token)

            base_path, pattern, fullpath, recursive = _extract_pathinfo(
                output_file.file_pattern)
            file_info.append(ResolvedFileMapping(
                base_path,
                pattern,
                fullpath,
                recursive,
                blob_client,
                container,
                destination.container.path))
        self.logger.info('Resolved mappings: [%s]', file_info)

        self.push_file_list_to_storage(file_info)
        self.logger.info('Done uploading, exiting...')
