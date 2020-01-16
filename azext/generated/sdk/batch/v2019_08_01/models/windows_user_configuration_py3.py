# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class WindowsUserConfiguration(Model):
    """Properties used to create a user Account on a Windows Compute Node.

    :param login_mode: The login mode for the user. The default value for
     VirtualMachineConfiguration Pools is 'batch' and for
     CloudServiceConfiguration Pools is 'interactive'. Possible values include:
     'batch', 'interactive'
    :type login_mode: str or ~azure.batch.models.LoginMode
    """

    _attribute_map = {
        'login_mode': {'key': 'loginMode', 'type': 'LoginMode'},
    }

    def __init__(self, *, login_mode=None, **kwargs) -> None:
        super(WindowsUserConfiguration, self).__init__(**kwargs)
        self.login_mode = login_mode
