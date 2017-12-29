# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps

# pylint: disable=line-too-long

helps['batch'] = """
    type: group
    short-summary: Manage Azure Batch.
"""

helps['batch job'] = """
    type: group
    short-summary: Manage Batch jobs.
"""

helps['batch job create'] = """
    type: command
    short-summary: Add a job and associated task(s) to a Batch account.
"""

helps['batch pool'] = """
    type: group
    short-summary: Manage Batch pools.
"""

helps['batch pool create'] = """
    type: command
    short-summary: Create a Batch pool in an account. When creating a pool, choose arguments from either Cloud Services Configuration or Virtual Machine Configuration.
"""

helps['batch file'] = """
    type: group
    short-summary: Manage Batch input files.
"""

helps['batch file upload'] = """
    type: command
    short-summary: Upload a specified file or directory of files to the specified storage path.
"""

helps['batch file download'] = """
    type: command
    short-summary: Download a specified file or directory of files to the specified storage path.
"""
