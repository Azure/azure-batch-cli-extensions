#!/usr/bin/env bash

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

set -e

scripts_root=$(cd $(dirname $0); pwd)

export PYTHONPATH=$PATHONPATH:./src
python -m azure.cli -h
check_style --ci;
run_tests

if [[ "$CI" == "true" ]]; then
    $scripts_root/package_verify.sh
fi

python $scripts_root/license/verify.py
