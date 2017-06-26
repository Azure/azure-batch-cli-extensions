#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


from codecs import open
from setuptools import setup

VERSION = '0.1.0'

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
    'azure-batch==3.0.0',
    'azure-mgmt-batch==4.0.0',
    'azure-storage==0.34.3',
    'azure-mgmt-storage==1.0.0'
]
DEPENDENCIES_27 = {
    ":python_version<'3.4'": ['pathlib>=1.0.1']
}


with open('README.rst', 'r', encoding='utf-8') as f:
    README = f.read()
with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    HISTORY = f.read()

setup(
    name='azure-batch-extensions',
    version=VERSION,
    description='Microsoft Azure Batch Extended Features',
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    author='Microsoft Corporation',
    author_email='askwabatch@microsoft.com',
    url='https://github.com/Azure/azure-batch-cli-extensions',
    classifiers=CLASSIFIERS,
    namespace_packages=[
        'azure'
    ],
    packages=[
        'azure.batch_extensions',
        'azure.batch_extensions.operations',
        'azure.batch_extensions.models'
    ],
    install_requires=DEPENDENCIES,
    extras_require=DEPENDENCIES_27,
)
