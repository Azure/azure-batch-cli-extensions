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
import argparse
import os
import json
import sys
import traceback

import uploader
import configuration

UPLOAD_LOG_NAME = 'uploadlog.txt'
_error_mapping = {
    # Bad request
    400: (configuration.ErrorCode.InternalError, False),
    # Unauthenticated
    403: (configuration.ErrorCode.AuthenticationFailed, True),
    # Not found
    404: (configuration.ErrorCode.ContainerNotFound, True),
    # Conflict
    409: (configuration.ErrorCode.Conflict, True),
    # Precondition failed
    412: (configuration.ErrorCode.PreconditionFailed, False),
    # Internal server error
    500: (configuration.ErrorCode.InternalError, False),
    # ServerBusy
    503: (configuration.ErrorCode.InternalError, False),
}


def load_specification_from_file(file_path):
    # type: str -> configuration.Specification
    """Loads a specification from a file path

    :param file_path: The path to load the specification from
    :return: The specification object
    """
    with open(file_path) as f:
        spec = json.load(f)
    return configuration.Specification.from_dict(spec)


def load_specification_from_env(env):
    # type: str -> configuration.Specification
    """Loads a specification from an environment variable.

    :param env: The name of the environment variable to load
    the specification from
    :return: The specification object
    """
    spec = json.loads(os.environ[env])
    return configuration.Specification.from_dict(spec)


def load_specification_from_stdin():
    # type: () -> configuration.Specification
    """Loads a specification from stdin

    :return: The specification object
    """
    spec = json.loads(sys.stdin.read())
    return configuration.Specification.from_dict(spec)


def generate_error_specification(exception):
    try:
        file, pattern, error = exception.errors[0]
        try:
            code, user_error = _error_mapping[error.status_code]
        except (KeyError, AttributeError):
            code, user_error = configuration.ErrorCode.UnknownError, False
        result = configuration.ErrorSpecification(
            code, user_error, pattern, file)
    except Exception:
        result = configuration.ErrorSpecification(
            configuration.ErrorCode.UnknownError, False, None, None)

    return result


def main():
    # parse args
    args = parseargs(sys.argv[1:])

    if args.file is not None:
        specification = load_specification_from_file(args.file)
    else:
        specification = load_specification_from_env(args.env)

    file_uploader = uploader.FileUploader(
        os.environ['AZ_BATCH_JOB_ID'],
        os.environ['AZ_BATCH_TASK_ID'])

    success = None
    if args.success:
        success = True
    if args.failure:
        success = False
    try:
        file_uploader.run(specification, success)
    except Exception as e:
        error_details = generate_error_specification(e)
        traceback.print_exc(file=sys.stdout)
        json.dump(error_details, sys.stderr)
        sys.exit(1)


def parseargs(args):
    parser = argparse.ArgumentParser(
        description='Azure Batch File uploader')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--file',
        help='File containing the upload specification.')
    group.add_argument(
        '--env',
        help='Environment variable containing the upload specification')
    success_failure_group = parser.add_mutually_exclusive_group()
    success_failure_group.add_argument(
        '-s', '--success',
        action='store_true',
        default=None,
        help='Specifies to upload files associated with TaskSuccess')
    success_failure_group.add_argument(
        '-f', '--failure',
        action='store_true',
        default=None,
        help='Specifies to upload files associated with TaskFailure')

    return parser.parse_args(args)


if __name__ == '__main__':
    main()
