#!/usr/bin/env python

from __future__ import print_function
import subprocess
import urllib2
import os
import sys

import util


def execute_commands(commands):
    """Executes a set of commands in sequence

    :param commands: The commands to execute
    """
    for command in commands:
        subprocess.check_call(command, shell=True)

if __name__ == '__main__':
    print('Current python version:')
    subprocess.check_call(['python', '-V', '2>&1'])

    # We don't have to pip install on windows since we installed
    # Python and that does it for us
    if not util.on_windows():
        response = urllib2.urlopen('https://bootstrap.pypa.io/get-pip.py')
        with open('get-pip.py', 'wb') as fd:
            fd.write(response.read())
        subprocess.check_call(['python', 'get-pip.py'])

    subprocess.check_call(['pip', 'install', 'virtualenv'])

    venv_loc = os.path.join(os.environ['AZ_BATCH_JOB_PREP_DIR'], 'batch-upload-venv')
    print('Creating virtual env at {}'.format(venv_loc))
    if not os.path.isdir(venv_loc):
        os.makedirs(venv_loc)
        subprocess.check_call(['virtualenv', venv_loc])

    pip_cmd = ['pip', 'install', '-r', 'requirements.txt']
    if util.on_windows():
        activate_script = os.path.join(venv_loc, 'Scripts', 'activate.bat')
        print('Activating venv: {}'.format(activate_script))
        subprocess.check_call([activate_script, '&&'] + pip_cmd)
    else:
        activate_script = os.path.join(venv_loc, 'bin', 'activate')
        print('Activating venv: {}'.format(activate_script))
        subprocess.check_call(['/bin/bash', '-c', 'source {} && {}'.format(
            activate_script,
            ' '.join(pip_cmd))])

    # Now invoke the other command lines required
    args = sys.argv[1:]
    execute_commands(args)
