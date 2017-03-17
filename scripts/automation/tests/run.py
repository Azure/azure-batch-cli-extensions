# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import argparse
import os
import sys

import automation.utilities.path as automation_path
from automation.utilities.path import filter_user_selected_modules_with_tests
from automation.tests.nose_helper import get_nose_runner
from automation.utilities.display import print_records
from automation.utilities.path import get_test_results_dir


def run_tests(parallel, run_live):
    print('\n\nRun automation')

    # create test results folder
    test_results_folder = get_test_results_dir(with_timestamp=True, prefix='tests')

    # get test runner
    run_nose = get_nose_runner(test_results_folder, xunit_report=True, exclude_integration=True,
                               parallel=parallel)

    # set environment variable
    if run_live:
        os.environ['AZURE_CLI_TEST_RUN_LIVE'] = 'True'

    # run tests
    passed = True
    module_results = []
    name = 'batch-extensions'
    test_path = os.path.join(automation_path.get_repo_root(), 'tests')
    result, start, end, _ = run_nose(name, test_path)
    passed &= result
    record = (name, start.strftime('%H:%M:%D'), str((end - start).total_seconds()),
              'Pass' if result else 'Fail')

    module_results.append(record)

    print_records(module_results, title='test results')

    return passed


if __name__ == '__main__':
    parse = argparse.ArgumentParser('Test tools')
    parse.add_argument('--non-parallel', action='store_true',
                       help='Not to run the tests in parallel.')
    parse.add_argument('--live', action='store_true', help='Run all the tests live.')
    args = parse.parse_args()

    retval = run_tests(not args.non_parallel, args.live)

    sys.exit(0 if retval else 1)
