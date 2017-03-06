#!/usr/bin/env python

from __future__ import print_function
import subprocess
import sys
import os
import util

if __name__ == '__main__':
    user_err = int(sys.argv[1])
    venv_loc = os.path.join(os.environ['AZ_BATCH_JOB_PREP_DIR'], 'batch-upload-venv')
    if util.on_windows():
        upload_command = [
            'cmd',
            '/c',
            '{} && python {}\\batchfileuploader.py '
            '--env AZ_BATCH_FILE_UPLOAD_CONFIG -{} > {}\\uploadlog.txt 2>&1'.format(
                os.path.join(venv_loc, 'scripts', 'activate'),
                os.environ['AZ_BATCH_JOB_PREP_WORKING_DIR'],
                's' if user_err == 0 else 'f',
                os.environ['AZ_BATCH_TASK_DIR'])]
    else:
        upload_command = [
            '/bin/bash',
            '-c',
            'source {} && python {}/batchfileuploader.py '
            '--env AZ_BATCH_FILE_UPLOAD_CONFIG -{} > {}/uploadlog.txt 2>&1'.format(
                os.path.join(venv_loc, 'bin', 'activate'),
                os.environ['AZ_BATCH_JOB_PREP_WORKING_DIR'],
                's' if user_err == 0 else 'f',
                os.environ['AZ_BATCH_TASK_DIR'])]
    subprocess.call(upload_command)

    sys.exit(user_err)
