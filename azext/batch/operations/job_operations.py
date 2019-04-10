# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
from __future__ import unicode_literals

import importlib
import logging

from msrest.exceptions import DeserializationError
from azure.batch.operations._job_operations import JobOperations

from .. import models
from .. import _template_utils
from .. import _pool_utils
from .._file_utils import FileUtils
from ..models.constants import SupportedRestApi, SupportRestApiToSdkVersion

logger = logging.getLogger(__name__)

class ExtendedJobOperations(JobOperations):
    """JobOperations operations.

    :param parent: The parent BatchExtensionsClient object.
    :param client: Client for service requests.
    :param config: Configuration of service client.
    :param serializer: An object model serializer.
    :param deserializer: An objec model deserializer.
    :param get_storage_account: A callable to retrieve a storage client object.
    """
    def __init__(self, parent, client, config, serializer, deserializer, get_storage_account):
        super(ExtendedJobOperations, self).__init__(client, config, serializer, deserializer)
        self._parent = parent
        self.get_storage_client = get_storage_account

    def _get_target_pool(self, job):
        """Retrieve the pool information associated with a job. If the job
        is an auto-pool, this will be the pool specification. Otherwise
        we will do a GET call on the pool ID.
        :param job: The job we want to extract the pool info from.
        :type job: :class:`JobAddParameter<azure.batch.models.JobAddParameter>` or
         :class:`ExtendedJobParameter<azext.batch.models.ExtendedJobParameter>`
        :returns: :class:`CloudPool<azure.batch.models.CloudPool>`
        """
        if not job.pool_info:
            raise ValueError('Missing required poolInfo.')
        if job.pool_info.pool_id:
            return self._parent.pool.get(job.pool_info.pool_id)
        if (job.pool_info.auto_pool_specification
                and job.pool_info.auto_pool_specification.pool):
            return job.pool_info.auto_pool_specification.pool
        raise ValueError('Missing required poolId or autoPoolSpecification.pool.')

    @staticmethod
    def expand_template(template, parameters=None):
        """Expand a JSON template, substituting in optional parameters.
        :param template: The template data. Must be a dictionary.
        :param parameters: The values of parameters to be substituted into
         the template. Must be a dictionary.
        :returns: The job specification JSON dictionary.
        """
        if not isinstance(template, dict):
            raise ValueError("template isn't a JSON dictionary")
        if parameters and not isinstance(parameters, dict):
            raise ValueError("parameters isn't a JSON dictionary")
        elif not parameters:
            parameters = {}
        expanded_job_object = _template_utils.expand_template(template, parameters)
        try:
            return expanded_job_object['job']
        except KeyError:
            raise ValueError("Template missing required 'job' element")

    @staticmethod
    def jobparameter_from_json(json_data):
        """Create an ExtendedJobParameter object from a JSON specification.
        :param dict json_data: The JSON specification of an AddJobParameter or an
         ExtendedJobParameter or a JobTemplate
        """
        # json_data = templates.convert_blob_source_to_http_url(json_data)
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
                return ExtendedJobOperations._jobparameter_from_json(
                    json_data,
                    vendored_models)
            else:
                logging.warning("Invalid apiVersion, defaulting to latest")
        return ExtendedJobOperations._jobparameter_from_json(
            json_data,
            models)

    @staticmethod
    def _jobparameter_from_json(json_data, models_impl):
        result = 'JobTemplate' if json_data.get('properties') else 'ExtendedJobParameter'
        try:
            if result == 'JobTemplate':
                job = models_impl.JobTemplate.from_dict(json_data)
            else:
                job = models_impl.ExtendedJobParameter.from_dict(json_data)
            if job is None:
                raise ValueError("JSON data is not in correct format.")
            return job
        except NotImplementedError:
            raise
        except Exception as exp:
            raise ValueError("Unable to deserialize to {}: {}".format(result, exp))

    # pylint: disable=arguments-differ
    def add(self, job, job_add_options=None, custom_headers=None, raw=False,
            threads=None, **operation_config):
        """Adds a job to the specified account.

        The Batch service supports two ways to control the work done as part of
        a job. In the first approach, the user specifies a Job Manager task.
        The Batch service launches this task when it is ready to start the job.
        The Job Manager task controls all other tasks that run under this job,
        by using the Task APIs. In the second approach, the user directly
        controls the execution of tasks under an active job, by using the Task
        APIs. Also note: when naming jobs, avoid including sensitive
        information such as user names or secret project names. This
        information may appear in telemetry logs accessible to Microsoft
        Support engineers.

        :param job: The job to be added.
        :type job: :class:`JobAddParameter<azure.batch.models.JobAddParameter>` or
         :class:`ExtendedJobParameter<azext.batch.models.ExtendedJobParameter>`
         or :class:`JobTemplate<azure.batch.models.JobTemplate>`
        :param job_add_options: Additional parameters for the operation
        :type job_add_options: :class:`JobAddOptions
         <azure.batch.models.JobAddOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param int threads: number of threads to use in parallel when adding tasks.
         If specified will start additional threads to submit requests and
         wait for them to finish. Defaults to half of cpu count(floor)
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` if using TaskFactory or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true, otherwise None
        :rtype: None or :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises:
         :class:`BatchErrorException<azure.batch.models.BatchErrorException>`
        """
        original_api_version = None
        api_version = None
        vendored_pool_utils = importlib.import_module("azext.batch._pool_utils")
        vendored_template_utils = importlib.import_module("azext.batch._template_utils")
        vendored_models = importlib.import_module("azext.batch.models")
        api_version_raw = getattr(job, 'api_version', None)
        if api_version_raw:
            for valid_version in SupportedRestApi:
                if api_version_raw in valid_version.value:
                    api_version = valid_version
                    break

            if api_version and SupportRestApiToSdkVersion[api_version] != "latest":
                vendor_base = "azext.batch._vendor.v{}.azext.batch".format(
                    SupportRestApiToSdkVersion[api_version])
                models_str = "{}.models".format(
                    vendor_base)
                vendored_models = importlib.import_module(models_str)

                pool_utils_str = "{}._pool_utils".format(
                    vendor_base)
                vendored_pool_utils = importlib.import_module(pool_utils_str)

                templates_str = "{}._template_utils".format(
                    vendor_base)
                vendored_template_utils = importlib.import_module(templates_str)

                if isinstance(job, vendored_models.JobTemplate):
                    job = job.properties
            else:
                logging.warning("Invalid apiVersion, defaulting to latest")
                api_version = None

        if isinstance(job, models.JobTemplate):
            job = job.properties

        try:
            if api_version:
                original_api_version = self.api_version
                self.api_version = api_version.value[0]
                self._parent.task.api_version = api_version.value[0]
                ret = self._add(
                    job,
                    job_add_options,
                    custom_headers,
                    raw,
                    threads,
                    vendored_pool_utils,
                    vendored_template_utils,
                    vendored_models,
                    **operation_config)
                self.api_version = original_api_version
                return ret
            return self._add(
                job,
                job_add_options,
                custom_headers,
                raw,
                threads,
                _pool_utils,
                _template_utils,
                models,
                **operation_config)
        except Exception as e:  # pylint: disable=broad-except
            if original_api_version:
                self.api_version = original_api_version
                self._parent.task.api_version = original_api_version
            raise e
    add.metadata = {'url': '/jobs'}

    def _add(self, job, job_add_options, custom_headers, raw,
             threads, pool_utils, template_utils, models_impl, **operation_config):
        """Adds a job to the specified account.

        The Batch service supports two ways to control the work done as part of
        a job. In the first approach, the user specifies a Job Manager task.
        The Batch service launches this task when it is ready to start the job.
        The Job Manager task controls all other tasks that run under this job,
        by using the Task APIs. In the second approach, the user directly
        controls the execution of tasks under an active job, by using the Task
        APIs. Also note: when naming jobs, avoid including sensitive
        information such as user names or secret project names. This
        information may appear in telemetry logs accessible to Microsoft
        Support engineers.

        :param job: The job to be added.
        :type job: :class:`JobAddParameter<azure.batch.models.JobAddParameter>` or
         :class:`ExtendedJobParameter<azext.batch.models.ExtendedJobParameter>`
         or :class:`JobTemplate<azure.batch.models.JobTemplate>`
        :param job_add_options: Additional parameters for the operation
        :type job_add_options: :class:`JobAddOptions
         <azure.batch.models.JobAddOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param int threads: number of threads to use in parallel when adding tasks.
         If specified will start additional threads to submit requests and
         wait for them to finish. Defaults to half of cpu count(floor)
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` if using TaskFactory or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true, otherwise None
        :rtype: None or :class:`TaskAddCollectionResult
         <azure.batch.models.TaskAddCollectionResult>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises:
         :class:`BatchErrorException<azure.batch.models.BatchErrorException>`
        """
        # Process an application template reference.
        if hasattr(job, 'application_template_info') and job.application_template_info:
            try:
                template_utils.expand_application_template(job, self._deserialize)
            except DeserializationError as error:
                raise ValueError("Failed to load application template from '{}': {}".
                                 format(job.application_template_info.file_path, error))

        # Process a task factory.
        auto_complete = False
        task_collection = []
        file_utils = FileUtils(self.get_storage_client)
        if hasattr(job, 'task_factory') and job.task_factory:
            if template_utils.has_merge_task(job):
                job.uses_task_dependencies = True
            task_collection = template_utils.expand_task_factory(job, file_utils)

            # If job has a task factory and terminate job on all tasks complete is set, the job will
            # already be terminated when we add the tasks, so we need to set to noAction, then patch
            # the job once the tasks have been submitted.
            if job.on_all_tasks_complete and job.on_all_tasks_complete != 'noAction':
                auto_complete = job.on_all_tasks_complete
                job.on_all_tasks_complete = 'noaction'

        should_get_pool = template_utils.should_get_pool(job, task_collection)
        pool_os_flavor = None
        if should_get_pool:
            pool = self._get_target_pool(job)
            pool_os_flavor = pool_utils.get_pool_target_os_type(pool)

        # Handle package management on autopool
        if job.pool_info.auto_pool_specification \
                and job.pool_info.auto_pool_specification.pool \
                and job.pool_info.auto_pool_specification.pool.package_references:

            pool = job.pool_info.auto_pool_specification.pool
            cmds = [template_utils.process_pool_package_references(pool)]
            pool.start_task = models_impl.StartTask(
                **template_utils.construct_setup_task(pool.start_task, cmds, pool_os_flavor))

        commands = []
        # Handle package management on tasks.
        commands.append(template_utils.process_task_package_references(
            task_collection, pool_os_flavor))
        job_prep_task_parameters = template_utils.construct_setup_task(
            job.job_preparation_task, commands, pool_os_flavor)
        if job_prep_task_parameters:
            job.job_preparation_task = models_impl.JobPreparationTask(**job_prep_task_parameters)

        # Handle any extended resource file references.
            template_utils.post_processing(job, file_utils, pool_os_flavor)
        if task_collection:
            template_utils.post_processing(task_collection, file_utils, pool_os_flavor)
            template_utils.process_job_for_output_files(job, task_collection, file_utils)

        # Begin original job add process
        result = super(ExtendedJobOperations, self).add(
            job, job_add_options, custom_headers, raw, **operation_config)
        if task_collection:
            try:
                tasks = self._parent.task.add_collection(
                    job.id,
                    task_collection,
                    None,
                    None,
                    raw,
                    threads)
            except Exception as e:
                # If task submission raises, we roll back the job
                self.delete(job.id)
                raise e
            if auto_complete:
                # If the option to terminate the job was set, we need to reapply it with a patch
                # now that the tasks have been added.
                self.patch(job.id, {'on_all_tasks_complete': auto_complete})
            return tasks
        return result
