# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.batch.operations.pool_operations import PoolOperations

from .. import models
from .. import _file_utils as file_utils
from .. import _pool_utils as pool_utils
from .. import _template_utils as templates


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
        expanded_pool_object = templates.expand_template(template, parameters)
        try:
            return expanded_pool_object['pool']
        except KeyError:
            raise ValueError("Template missing required 'pool' element")

    def poolparameter_from_json(self, json_data):
        """Create an ExtendedPoolParameter object from a JSON specification.
        :param dict json_data: The JSON specification of an AddPoolParameter or an
         ExtendedPoolParameter or a PoolTemplate.
        """
        result = 'PoolTemplate' if json_data.get('properties') else 'ExtendedPoolParameter'
        try:
            pool = self._deserialize(result, json_data)
            if pool is None:
                raise ValueError("JSON data is not in correct format.")
            return pool
        except Exception as exp:
            raise ValueError("Unable to deserialize to {}: {}".format(result, exp))

    def add(
            self, pool, pool_add_options=None, custom_headers=None, raw=False, **operation_config):
        """Adds a pool to the specified account.

        When naming pools, avoid including sensitive information such as user
        names or secret project names. This information may appear in telemetry
        logs accessible to Microsoft Support engineers.

        :param pool: The pool to be added.
        :type pool: :class:`PoolAddParameter<azure.batch.models.PoolAddParameter>` or
         :class:`ExtendedPoolParameter<azure.batch_extensions.models.ExtendedPoolParameter>`
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
        if isinstance(pool, models.PoolTemplate):
            pool = pool.properties
        pool_os_flavor = pool_utils.get_pool_target_os_type(pool)
        # Handle package manangement
        if hasattr(pool, 'package_references') and pool.package_references:
            cmds = [templates.process_pool_package_references(pool)]
            # Update the start task command
            pool.start_task = models.StartTask(**templates.construct_setup_task(
                pool.start_task, cmds, pool_os_flavor))

        # Handle any extended resource file references.
        fileutils = file_utils.FileUtils(self.get_storage_client)
        templates.post_processing(pool, fileutils, pool_os_flavor)

        return super(ExtendedPoolOperations, self).add(pool, pool_add_options, custom_headers, raw, **operation_config)
    add.metadata = {'url': '/pools'}
