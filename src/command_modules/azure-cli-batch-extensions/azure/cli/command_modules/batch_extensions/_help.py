# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.core.help_files import helps

# pylint: disable=line-too-long

helps['batch'] = """
    type: group
    short-summary: Commands for working with Azure Batch.
"""

helps['batch job'] = """
    type: group
    short-summary: Commands to manage your Batch jobs.
"""

helps['batch job create'] = """
    type: command
    short-summary: Adds a job and associated task(s) to the specified account.
"""

helps['batch pool'] = """
    type: group
    short-summary: Commands to manage your Batch pools.
"""

helps['batch pool create'] = """
    type: command
    short-summary: Create a Batch pool.
"""

helps['batch file'] = """
    type: group
    short-summary: Commands to manage your Batch input files.
"""

helps['batch file upload'] = """
    type: command
    short-summary: Upload a specified file or directory of files to the specified storage path.
"""

helps['batch file download'] = """
    type: command
    short-summary: Download a specified file or directory of files to the specified storage path.
"""
