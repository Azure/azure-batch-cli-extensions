# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

class MissingParameterValue(ValueError):

    def __init__(self, message, parameter_name=None, parameter_description=None):
        self.parameter_name = parameter_name
        self.parameter_description = parameter_description
        super(MissingParameterValue, self).__init__(message)
