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


class AuthenticationTokenSettings(Model):
    """The settings for an authentication token that the Task can use to perform
    Batch service operations.

    :param access: The Batch resources to which the token grants access. The
     authentication token grants access to a limited set of Batch service
     operations. Currently the only supported value for the access property is
     'job', which grants access to all operations related to the Job which
     contains the Task.
    :type access: list[str or ~azure.batch.models.AccessScope]
    """

    _attribute_map = {
        'access': {'key': 'access', 'type': '[AccessScope]'},
    }

    def __init__(self, **kwargs):
        super(AuthenticationTokenSettings, self).__init__(**kwargs)
        self.access = kwargs.get('access', None)
