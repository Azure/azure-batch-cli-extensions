# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""Verify the command modules by install them using PIP"""

from __future__ import print_function

import os
import shutil
import os.path
import tempfile
import subprocess
import sys
import pip
import imp
import fileinput
import importlib

import automation.utilities.path as automation_path
from automation.utilities.display import print_heading
from automation.utilities.const import COMMAND_MODULE_PREFIX


def exec_command(command, cwd=None, stdout=None, env=None):
    """Returns True in the command was executed successfully"""
    try:
        command_list = command if isinstance(command, list) else command.split()
        env_vars = os.environ.copy()
        if env:
            env_vars.update(env)
        subprocess.check_call(command_list, stdout=stdout, cwd=cwd, env=env_vars)
        return True
    except subprocess.CalledProcessError as err:
        print(err, file=sys.stderr)
        return False


def set_version(path_to_setup):
    """
    Give package a high version no. so when we install, we install this one and not a version from
    PyPI
    """
    for _, line in enumerate(fileinput.input(path_to_setup, inplace=1)):
        line = line.replace('version=VERSION', "version='1000.0.0'")
        line = line.replace('azure-batch-extensions>=0.1,<1', 'azure-batch-extensions==1000.0.0')
        sys.stdout.write(line)


def reset_version(path_to_setup):
    """
    Revert package to original version no. for PyPI package and deploy.
    """
    for _, line in enumerate(fileinput.input(path_to_setup, inplace=1)):
        line = line.replace("version='1000.0.0'", 'version=VERSION')
        line = line.replace('azure-batch-extensions==1000.0.0', 'azure-batch-extensions>=0.1,<1')
        sys.stdout.write(line)


def build_package(path_to_package, dist_dir):
    print_heading('Building {}'.format(path_to_package))
    path_to_setup = os.path.join(path_to_package, 'setup.py')
    set_version(path_to_setup)
    cmd_success = exec_command('python setup.py sdist -d {0} bdist_wheel -d {0}'.format(dist_dir), cwd=path_to_package)
    if not cmd_success:
        print_heading('Error building {}!'.format(path_to_package), f=sys.stderr)
        sys.exit(1)
    reset_version(path_to_setup)
    print('reset setup version')
    print_heading('Built {}'.format(path_to_package))


def install_pip_package(package_name):
    print_heading('Installing {}'.format(package_name))
    cmd = 'python -m pip install {}'.format(package_name)
    cmd_success = exec_command(cmd)
    if not cmd_success:
        print_heading('Error installing {}!'.format(package_name), f=sys.stderr)
        sys.exit(1)
    print_heading('Installed {}'.format(package_name))


def install_package(path_to_package, package_name, dist_dir):
    egg_path = os.path.join(path_to_package, '{}.egg-info'.format(package_name.replace('-', '_')))
    print("deleting {}".format(egg_path))
    try:
        shutil.rmtree(egg_path)
    except Exception as exp:
        print("Couldn't delete: {}".format(exp))
    print("deleting {}".format(os.path.join(path_to_package, 'build')))
    try:
        shutil.rmtree(os.path.join(path_to_package, 'build'))
    except Exception as exp:
        print("Couldn't delete: {}".format(exp))
    print_heading('Installing {}'.format(path_to_package))
    cmd = 'python -m pip install --upgrade {} --find-links file://{}'.format(package_name, dist_dir)
    cmd_success = exec_command(cmd)
    if not cmd_success:
        print_heading('Error installing {}!'.format(path_to_package), f=sys.stderr)
        sys.exit(1)
    print_heading('Installed {}'.format(path_to_package))


def verify_packages():
    # tmp dir to store all the built packages
    built_packages_dir = tempfile.mkdtemp()

    all_modules = automation_path.get_all_module_paths()

    # STEP 1:: Install the CLI and dependencies by pip
    install_pip_package('azure-cli')

    # STEP 2:: Build the packages
    for name, path in all_modules:
        build_package(path, built_packages_dir)

    # STEP 3:: Install Batch Extensions and validate
    install_package(all_modules[0][1], all_modules[0][0], built_packages_dir) 
    try:
        importlib.import_module('azure.batch_extensions')
    except ImportError as err:
        print("Unable to import {}".format(name))
        print(err)
        sys.exit(1)

    # STEP 4:: Add CLI extension wheel to CLI
    # try: 

    #     extension_whl = os.path.join(built_packages_dir, 'azure_batch_cli_extensions-1000.0.0-py2.py3-none-any.whl')
    #     az_output = subprocess.check_output(['az', 'extension', 'add', '--source', extension_whl, '--debug'], stderr=subprocess.STDOUT,
    #                                         universal_newlines=True)
    #     success = 'Successfully installed azure-batch-cli-extensions-1000.0.0' in az_output
    #     print(az_output, file=sys.stderr)
    # except subprocess.CalledProcessError as err:
    #     success = False
    #     print(err, file=sys.stderr)

    # STEP 5:: Verify extension loading correctly
    try:
        az_output = subprocess.check_output(['az', '--debug'], stderr=subprocess.STDOUT,
                                            universal_newlines=True)
        success = 'Error loading command module' not in az_output
        if success:
            success = 'Loaded extension \'azure-batch-cli-extensions\'' in az_output
        print(az_output, file=sys.stderr)
    except subprocess.CalledProcessError as err:
        success = False
        print(err, file=sys.stderr)

    if not success:
        print_heading('Error running the CLI!', f=sys.stderr)
        sys.exit(1)

    pip.utils.pkg_resources = imp.reload(pip.utils.pkg_resources)
    installed_modules = [dist.key for dist in
                         pip.get_installed_distributions(local_only=True)]

    print('Installed command modules', installed_modules)

    missing_modules = \
        set([all_modules[0][0]]) - set(installed_modules)

    if missing_modules:
        print_heading('Error: The following modules were not installed successfully', f=sys.stderr)
        print(missing_modules, file=sys.stderr)
        sys.exit(1)

    print_heading('OK')


if __name__ == '__main__':
    verify_packages()
