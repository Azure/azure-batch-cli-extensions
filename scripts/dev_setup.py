#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import print_function

import sys
import os
from subprocess import check_call, CalledProcessError

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
print(os.environ)
print('Root directory \'{}\'\n'.format(root_dir))

# install general requirements
exec_command('pip install -r requirements.txt')

# install to edge build of azure-cli
exec_command('pip install --pre azure-cli --extra-index-url https://azurecliprod.blob.core.windows.net/edge --no-cache-dir')

# upgrade to latest azure-batch
exec_command('pip install --upgrade azure-batch')

# install automation package
exec_command('pip install --upgrade -e ./scripts')

# install reference to extension module package
exec_command('pip install -e {}'.format(root_dir))
exec_command('pip install --upgrade --target ./.azure/devcliextensions/azure-batch-cli-extensions {0}'.format(root_dir))
exec_command('pip install --no-deps --upgrade --target ./.azure/devcliextensions/azure-batch-cli-extensions {0}/batch-cli-extensions'.format(root_dir))

print('Finished dev setup.')
