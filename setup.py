#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import re
from codecs import open
from setuptools import setup

# The full list of classifiers is available at
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = [
    'msrestazure>=0.4.14,<1',
    'azure-batch>=9.0,<10',
    'azure-mgmt-batch>=7.0,<8',
    'azure-storage-blob>=1.1.0,<2',
    'azure-mgmt-storage>=2.0,<3'
]
DEPENDENCIES_27 = {
    ":python_version<'3.4'": ['pathlib>=1.0.1']
}

# Version extraction inspired from 'requests'
with open(os.path.join('azext/batch', 'version.py'), 'r') as fd:
    version = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', 'r', encoding='utf-8') as f:
    README = f.read()
with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    HISTORY = f.read()

setup(
    name='azure-batch-extensions',
    version=version,
    description='Microsoft Azure Batch Extended Features',
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    author='Microsoft Corporation',
    author_email='azpycli@microsoft.com',
    url='https://github.com/Azure/azure-batch-cli-extensions',
    classifiers=CLASSIFIERS,
    namespace_packages=[
        'azext'
    ],
    packages=[
        'azext.batch',
        'azext.batch.operations',
        'azext.batch.models'
    ],
    install_requires=DEPENDENCIES,
    extras_require=DEPENDENCIES_27,
)
