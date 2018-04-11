# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from __future__ import unicode_literals

from msrest.exceptions import DeserializationError
from azure.batch.operations.job_operations import JobOperations

from .. import models
from .. import _template_utils as templates
from .. import _pool_utils as pool_utils
from .._file_utils import FileUtils


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
         :class:`ExtendedJobParameter<azure.batch_extensions.models.ExtendedJobParameter>`
        :returns: :class:`CloudPool<azure.batch.models.CloudPool>`
        """
        if not job.pool_info:
            raise ValueError('Missing required poolInfo.')
        if job.pool_info.pool_id:
            return self._parent.pool.get(job.pool_info.pool_id)
        elif job.pool_info.auto_pool_specification \
                and job.pool_info.auto_pool_specification.pool:
            return job.pool_info.auto_pool_specification.pool
        else:
            raise ValueError('Missing required poolId or autoPoolSpecification.pool.')

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
        expanded_job_object = templates.expand_template(template, parameters)
        try:
            return expanded_job_object['job']
        except KeyError:
            raise ValueError("Template missing required 'job' element")

    def jobparameter_from_json(self, json_data):
        """Create an ExtendedJobParameter object from a JSON specification.
        :param dict json_data: The JSON specification of an AddJobParameter or an
         ExtendedJobParameter or a JobTemplate
        """
        result = 'JobTemplate' if json_data.get('properties') else 'ExtendedJobParameter'
        try:
            job = self._deserialize(result, json_data)
            if job is None:
                raise ValueError("JSON file is not in correct format.")
            return job
        except Exception as exp:
            raise ValueError("Unable to deserialize to {}: {}".format(result, exp))

    def add(self, job, job_add_options=None, custom_headers=None, raw=False, **operation_config):
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
         :class:`ExtendedJobParameter<azure.batch_extensions.models.ExtendedJobParameter>`
         or :class:`JobTemplate<azure.batch.models.JobTemplate>`
        :param job_add_options: Additional parameters for the operation
        :type job_add_options: :class:`JobAddOptions
         <azure.batch.models.JobAddOptions>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
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
        if isinstance(job, models.JobTemplate):
            job = job.properties
        # Process an application template reference.
        if hasattr(job, 'application_template_info') and job.application_template_info:
            try:
                templates.expand_application_template(job, self._deserialize)
            except DeserializationError as error:
                raise ValueError("Failed to load application template from '{}': {}".
                                 format(job.application_template_info.file_path, error))

        # Process a task factory.
        auto_complete = False
        task_collection = []
        file_utils = FileUtils(self.get_storage_client)
        if hasattr(job, 'task_factory') and job.task_factory:
            task_collection = templates.expand_task_factory(job, file_utils)

            # If job has a task factory and terminate job on all tasks complete is set, the job will
            # already be terminated when we add the tasks, so we need to set to noAction, then patch
            # the job once the tasks have been submitted.
            if job.on_all_tasks_complete and job.on_all_tasks_complete != 'noAction':
                auto_complete = job.on_all_tasks_complete
                job.on_all_tasks_complete = 'noaction'

        should_get_pool = templates.should_get_pool(job, task_collection)
        pool_os_flavor = None
        if should_get_pool:
            pool = self._get_target_pool(job)
            pool_os_flavor = pool_utils.get_pool_target_os_type(pool)

        # Handle package management on autopool
        if job.pool_info.auto_pool_specification \
                and job.pool_info.auto_pool_specification.pool \
                and job.pool_info.auto_pool_specification.pool.package_references:

            pool = job.pool_info.auto_pool_specification.pool
            cmds = [templates.process_pool_package_references(pool)]
            pool.start_task = models.StartTask(
                **templates.construct_setup_task(pool.start_task, cmds, pool_os_flavor))

        commands = []
        # Handle package management on tasks.
        commands.append(templates.process_task_package_references(
            task_collection, pool_os_flavor))
        job_prep_task_parameters = templates.construct_setup_task(
            job.job_preparation_task, commands, pool_os_flavor)
        if job_prep_task_parameters:
            job.job_preparation_task = models.JobPreparationTask(**job_prep_task_parameters)

        # Handle any extended resource file references.
        templates.post_processing(job, file_utils, pool_os_flavor)
        if task_collection:
            templates.post_processing(task_collection, file_utils, pool_os_flavor)
        templates.process_job_for_output_files(job, task_collection, file_utils)

        # Begin original job add process
        result = super(ExtendedJobOperations, self).add(
            job, job_add_options, custom_headers, raw, **operation_config)
        if task_collection:
            try:
                tasks = self._parent.task.add_collection(job.id, task_collection)
            except Exception:
                # If task submission raises, we roll back the job
                self.delete(job.id)
                raise
            if auto_complete:
                # If the option to terminate the job was set, we need to reapply it with a patch
                # now that the tasks have been added.
                self.patch(job.id, {'on_all_tasks_complete': auto_complete})
            return tasks
        return result
    add.metadata = {'url': '/jobs'}
