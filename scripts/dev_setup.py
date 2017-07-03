#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import sys
import os
from subprocess import check_call, CalledProcessError

modules = ['batch-extensions', 'batch-cli-extensions']
root_dir = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..'))


def exec_command(command):
    try:
        print('Executing: ' + command)
        check_call(command.split(), cwd=root_dir)
        print()
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        sys.exit(1)

print('Running dev setup...')
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements and azure-cli
exec_command('pip install -r requirements.txt')

# install automation package
exec_command('pip install -e ./scripts')

for m in modules:
  # install reference to extension module package
  exec_command('pip install -e {}'.format(os.path.join(root_dir, m)))

print('Finished dev setup.')
