# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import importlib
import logging

from azure.batch.operations.pool_operations import PoolOperations
from datetime import datetime as dt
from azure.batch.operations._pool_operations import PoolOperations
from mock import patch
from msrest import Serializer, Deserializer

from .. import models
from ..models.constants import *
from .. import _file_utils
from .. import _pool_utils
from .. import _template_utils

logger = logging.getLogger(__name__)

class ExtendedPoolOperations(PoolOperations):
    """PoolOperations operations.

    :param parent: The parent BatchExtensionsClient object.
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :param get_storage_account: A callable to retrieve a storage client object.
    """
    def __init__(self, parent, client, config, serializer, deserializer, get_storage_account):
        super(ExtendedPoolOperations, self).__init__(client, config, serializer, deserializer)
        self._parent = parent
        self.get_storage_client = get_storage_account

    @staticmethod
    def expand_template(template, parameters=None):
        """Expand a JSON template, substituting in optional parameters.
        :param template: The template data. Must be a dictionary.
        :param parameters: The values of parameters to be substituted into
         the template. Must be a dictionary.
        :returns: The pool specification JSON dictionary.
        """
        if not isinstance(template, dict):
            raise ValueError("template isn't a JSON dictionary")
        if parameters and not isinstance(parameters, dict):
            raise ValueError("parameters isn't a JSON dictionary")
        elif not parameters:
            parameters = {}
        expanded_pool_object = _template_utils.expand_template(template, parameters)
        try:
            # If JobParameter only return content
            return expanded_pool_object['pool']
        except KeyError:
            # Else return full template
            return expanded_pool_object

    @staticmethod
    def poolparameter_from_json(json_data):
        """Create an ExtendedPoolParameter object from a JSON specification.
        :param dict json_data: The JSON specification of an AddPoolParameter or an
         ExtendedPoolParameter or a PoolTemplate.
        """
        api_version_raw = json_data.get('apiVersion')
        if api_version_raw:
            api_version = None
            for valid_version in SupportedRestApi:
                if api_version_raw in valid_version.value:
                    api_version = valid_version
                    break

            if api_version and SupportRestApiToSdkVersion[api_version] != "latest":
                vendor_base = "azext.batch._vendor.v{}.azext.batch".format(
                    SupportRestApiToSdkVersion[api_version])
                models_str = "{}.models".format(vendor_base)
                vendored_models = importlib.import_module(models_str)
                return ExtendedPoolOperations._poolparameter_from_json(json_data, vendored_models)
            else:
                logging.warning("Invalid apiVersion, defaulting to latest")
        return ExtendedPoolOperations._poolparameter_from_json(json_data, models)


    @staticmethod
    def _poolparameter_from_json(json_data, models_impl):
        """Create an ExtendedPoolParameter object from a JSON specification.
        :param dict json_data: The JSON specification of an AddPoolParameter or an
         ExtendedPoolParameter or a PoolTemplate.
        :param module models: models to deserialize from
        """
        result = 'PoolTemplate' if json_data.get('properties') else 'ExtendedPoolParameter'
        try:
            if result == 'PoolTemplate':
                pool = models_impl.PoolTemplate.from_dict(json_data)
            else:
                pool = models_impl.ExtendedPoolParameter.from_dict(json_data)
            if pool is None:
                raise ValueError("JSON data is not in correct format.")
            return pool
        except NotImplementedError:
            raise
        except Exception as exp:
            raise ValueError("Unable to deserialize to {}: {}".format(result, exp))

    def add(self, pool, pool_add_options=None, custom_headers=None, raw=False, **operation_config):
        """Adds a pool to the specified account.

        When naming pools, avoid including sensitive information such as user
        names or secret project names. This information may appear in telemetry
        logs accessible to Microsoft Support engineers.

        :param pool: The pool to be added.
        :type pool: :class:`PoolAddParameter<azure.batch.models.PoolAddParameter>` or
         :class:`ExtendedPoolParameter<azext.batch.models.ExtendedPoolParameter>`
         or :class:`PoolTemplate<azure.batch.models.PoolTemplate>`
        :param pool_add_options: Additional parameters for the operation
        :type pool_add_options: :class:`PoolAddOptions
         <azure.batch.models.PoolAddOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises:
         :class:`BatchErrorException<azure.batch.models.BatchErrorException>`
        """
        original_api_version = None
        api_version = None
        vendored_pool_utils = None
        vendored_file_utils = None
        vendored_template_utils = None
        vendored_models = None

        api_version_raw = getattr(pool, 'api_version', None)
        if api_version_raw:
            for valid_version in SupportedRestApi:
                if api_version_raw in valid_version.value:
                    api_version = valid_version
                    break

            if not api_version:
                logging.warning("Invalid apiVersion, defaulting to latest")

            if api_version and SupportRestApiToSdkVersion[api_version] != "latest":
                vendor_base = "azext.batch._vendor.v{}.azext.batch".format(
                    SupportRestApiToSdkVersion[api_version])

                models_str = "{}.models".format(vendor_base)
                vendored_models = importlib.import_module(models_str)

                pool_utils_str = "{}._pool_utils".format(vendor_base)
                vendored_pool_utils = importlib.import_module(pool_utils_str)

                file_utils_str = "{}._file_utils".format(vendor_base)
                vendored_file_utils = importlib.import_module(file_utils_str)

                template_utils_str = "{}._template_utils".format(
                    vendor_base)
                vendored_template_utils = importlib.import_module(
                    template_utils_str)

                if isinstance(pool, vendored_models.PoolTemplate):
                    pool = pool.properties
            else:
                api_version = None
                logging.warning("Invalid apiVersion, defaulting to latest")

        if isinstance(pool, models.PoolTemplate):
            pool = pool.properties

        try:
            if api_version:
                original_api_version = self.api_version
                self.api_version = api_version.value[0]
                ret = self._add(
                    pool,
                    pool_add_options,
                    custom_headers,
                    raw,
                    vendored_pool_utils,
                    vendored_template_utils,
                    vendored_file_utils,
                    vendored_models,
                    **operation_config)
                self.api_version = original_api_version
                return ret
            else:
                return self._add(
                    pool,
                    pool_add_options,
                    custom_headers,
                    raw,
                    _pool_utils,
                    _template_utils,
                    _file_utils,
                    models,
                    **operation_config)
        except Exception:
            if original_api_version:
                self.api_version = original_api_version
                raise
    add.metadata = {'url': '/pools'}

    def _add(self,
             pool,
             pool_add_options,
             custom_headers,
             raw,
             pool_utils,
             template_utils,
             file_utils,
             models_impl,
             **operation_config):
        """ Internal add method for pool

        :param pool: The pool to be added.
        :type pool: :class:`PoolAddParameter<azure.batch.models.PoolAddParameter>` or
         :class:`ExtendedPoolParameter<azext.batch.models.ExtendedPoolParameter>`
         or :class:`PoolTemplate<azure.batch.models.PoolTemplate>`
        :param pool_add_options: Additional parameters for the operation
        :type pool_add_options: :class:`PoolAddOptions
         <azure.batch.models.PoolAddOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :param pool_utils: pool utility methods
        :param template_utils: template utility methods
        :param file_utils: file utility methods
        :return: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises:
         :class:`BatchErrorException<azure.batch.models.BatchErrorException>`
        """
        pool_os_flavor = pool_utils.get_pool_target_os_type(pool)
        # Handle package manangement
        if hasattr(pool, 'package_references') and pool.package_references:
            cmds = [template_utils.process_pool_package_references(pool)]
            # Update the start task command
            pool.start_task = models_impl.StartTask(**template_utils.construct_setup_task(
                pool.start_task, cmds, pool_os_flavor))

        # Handle any extended resource file references.
        fileutils = file_utils.FileUtils(self.get_storage_client)
        template_utils.post_processing(pool, fileutils, pool_os_flavor)

        return super(ExtendedPoolOperations, self).add(pool, pool_add_options,
                                                       custom_headers, raw,
                                                       **operation_config)

