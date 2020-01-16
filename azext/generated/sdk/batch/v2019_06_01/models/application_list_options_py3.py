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


class ApplicationListOptions(Model):
    """Additional parameters for list operation.

    :param max_results: The maximum number of items to return in the response.
     A maximum of 1000 applications can be returned. Default value: 1000 .
    :type max_results: int
    :param timeout: The maximum time that the server can spend processing the
     request, in seconds. The default is 30 seconds. Default value: 30 .
    :type timeout: int
    :param client_request_id: The caller-generated request identity, in the
     form of a GUID with no decoration such as curly braces, e.g.
     9C4D50EE-2D56-4CD3-8152-34347DC9F2B0.
    :type client_request_id: str
    :param return_client_request_id: Whether the server should return the
     client-request-id in the response. Default value: False .
    :type return_client_request_id: bool
    :param ocp_date: The time the request was issued. Client libraries
     typically set this to the current system clock time; set it explicitly if
     you are calling the REST API directly.
    :type ocp_date: datetime
    """

    _attribute_map = {
        'max_results': {'key': '', 'type': 'int'},
        'timeout': {'key': '', 'type': 'int'},
        'client_request_id': {'key': '', 'type': 'str'},
        'return_client_request_id': {'key': '', 'type': 'bool'},
        'ocp_date': {'key': '', 'type': 'rfc-1123'},
    }

    def __init__(self, *, max_results: int=1000, timeout: int=30, client_request_id: str=None, return_client_request_id: bool=False, ocp_date=None, **kwargs) -> None:
        super(ApplicationListOptions, self).__init__(**kwargs)
        self.max_results = max_results
        self.timeout = timeout
        self.client_request_id = client_request_id
        self.return_client_request_id = return_client_request_id
        self.ocp_date = ocp_date
