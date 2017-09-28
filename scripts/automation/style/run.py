# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import argparse
import multiprocessing
import os
import os.path
import sys
from subprocess import call
from distutils.sysconfig import get_python_lib

import automation.utilities.path as automation_path

def run_pylint():
    print('\n\nRun pylint')

    modules = [os.path.join(automation_path.get_repo_root(), 'azure')]
    modules.append(os.path.join(automation_path.get_repo_root(), 'batch-cli-extensions', 'azext_batch'))
    modules_list = ' '.join(modules)
    print(modules_list)
    arguments = '{} --rcfile={} -j {} -r n -d I0013'.format(
        modules_list,
        os.path.join(automation_path.get_repo_root(), 'pylintrc'),
        multiprocessing.cpu_count())

    return_code = call(('python -m pylint ' + arguments).split())

    if return_code:
        print('Pylint failed')
    else:
        print('Pylint passed')

    return return_code


def run_pep8():
    print('\n\nRun flake8 for PEP8 compliance')
    modules_list = ' '.join([os.path.join(automation_path.get_repo_root(), m) for m in MODULES])
    print(modules_list)
    command = 'flake8 --statistics --append-config={} {}'.format(
        os.path.join(automation_path.get_repo_root(), '.flake8'), modules_list)

    return_code = call(command.split())
    if return_code:
        print('Flake8 failed')
    else:
        print('Flake8 passed')

    return return_code


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Code style tools')
    parser.add_argument('--ci', action='store_true', help='Run in CI mode')
    parser.add_argument('--pep8', dest='suites', action='append_const', const='pep8',
                        help='Run flake8 to check PEP8')
    parser.add_argument('--pylint', dest='suites', action='append_const', const='pylint',
                        help='Run pylint')
    args = parser.parse_args()

    if args.ci:
        # Run pylint on all modules
        return_code_sum = run_pylint()

        sys.exit(return_code_sum)

    if not args.suites or not any(args.suites):
        return_code_sum = run_pylint()
    else:
        return_code_sum = 0
        if 'pep8' in args.suites:
            return_code_sum += run_pep8()

        if 'pylint' in args.suites:
            return_code_sum += run_pylint()

    sys.exit(return_code_sum)
