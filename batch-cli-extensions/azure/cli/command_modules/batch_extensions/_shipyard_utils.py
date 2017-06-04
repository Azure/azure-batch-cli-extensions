# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


import datetime

AZURE_FILE_VOLUME_TYPE = 'azurefile'


def _get_autostorage_credentials_label():
    """Gets the label of the AutoStorage account to use in the credentials.json file.
    :returns: The label of the AutoStorage account to use in the credentials.json file.
    """
    return 'autostorage_account'


def _generate_datavolume_label(task_id, datavolume_index):
    """Generates a label for a task data volume.
    :returns: A label for a task data volume based on the task id
     and the index of the data volume.
    """
    return str(task_id) + '_' + str(datavolume_index)


def _generate_temp_config_dir_name():
    """Generates a name for a temporary directory to hold the Batch Shipyard config files.
    This function uses the current time to create a directory name. If the user performs
    multiple invocations of the script within less than < .001 seconds, there will be a
    conflict.
    :returns: A temporary directory name based on the current time.
    """
    now = datetime.datetime.now()
    formatted_datestring = now.isoformat()
    # ISO format is YYYY-MM-DDTHH:mm:ss.sssZ
    # Replace all ':' chars with '.' chars to get a cleaner dir name.
    formatted_datestring = formatted_datestring.replace(':', '.')
    return 'BatchShipyardConfigs_' + formatted_datestring
