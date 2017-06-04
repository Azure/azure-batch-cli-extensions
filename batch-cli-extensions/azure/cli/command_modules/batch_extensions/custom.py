# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os
import errno

from azure.batch.models import (
    PoolAddParameter, CloudServiceConfiguration, VirtualMachineConfiguration,
    ImageReference, PoolInformation, JobAddParameter, JobManagerTask,
    JobConstraints, StartTask, JobAddOptions, PoolAddOptions)
from azure.cli.command_modules.batch_extensions._file_utils import (
    FileUtils, resolve_file_paths, upload_blob, resolve_remote_paths, download_blob)
import azure.cli.command_modules.batch_extensions._template_utils as template_utils
import azure.cli.command_modules.batch_extensions._pool_utils as pool_utils
import azure.cli.command_modules.batch_extensions._job_utils as job_utils
import azure.cli.core.azlogging as azlogging

logger = azlogging.get_az_logger(__name__)

# NCJ custom commands


def create_pool(client, account_name=None, account_endpoint=None,  # pylint:disable=too-many-arguments, too-many-locals
                template=None, parameters=None, json_file=None,
                id=None, vm_size=None, target_dedicated=None, auto_scale_formula=None,  # pylint: disable=redefined-builtin
                enable_inter_node_communication=False, os_family=None, image=None,
                node_agent_sku_id=None, resize_timeout=None, start_task_command_line=None,
                start_task_resource_files=None, start_task_wait_for_success=False,
                certificate_references=None, application_package_references=None, metadata=None):
    # pylint: disable=too-many-branches, too-many-statements
    if template or json_file:
        if template:
            logger.warning('You are using an experimental feature {Pool Template}.')
            expanded_pool_object = template_utils.expand_template(template, parameters)
            if 'pool' not in expanded_pool_object:
                raise ValueError('Missing pool element in the template.')
            if 'properties' not in expanded_pool_object['pool']:
                raise ValueError('Missing pool properties element in the template.')
            # bulid up the jsonFile object to hand to the batch service.
            json_obj = expanded_pool_object['pool']['properties']
        else:
            with open(json_file) as f:
                json_obj = json.load(f)
            # validate the json file
            pool = client._deserialize('PoolAddParameter', json_obj)  # pylint:disable=protected-access
            if pool is None:
                raise ValueError("JSON file '{}' is not in correct format.".format(json_file))

        # Handle package manangement
        if 'packageReferences' in json_obj:
            logger.warning('You are using an experimental feature {Package Management}.')
            pool_os_flavor = pool_utils.get_pool_target_os_type(json_obj)
            cmds = [template_utils.process_pool_package_references(json_obj)]
            # Update the start up command
            json_obj['startTask'] = template_utils.construct_setup_task(
                json_obj.get('startTask'), cmds, pool_os_flavor)

        # Handle any special post-processing steps.
        # - Resource Files
        # - etc
        file_utils = FileUtils(None, account_name, None, account_endpoint)
        json_obj = template_utils.post_processing(json_obj, file_utils)

        # Batch Shipyard integration
        if 'clientExtensions' in json_obj and 'dockerOptions' in json_obj['clientExtensions']:
            logger.warning('You are using an experimental feature {Batch Shipyard}.')
            # batchShipyardUtils.createPool(json_obj, options, cli)
            # return

        # We deal all NCJ work with pool, now convert back to original type
        pool = client._deserialize('PoolAddParameter', json_obj)  # pylint: disable=protected-access

    else:
        if not id:
            raise ValueError('Need either template, json_file, or id')

        pool = PoolAddParameter(id, vm_size=vm_size)
        if auto_scale_formula:
            pool.auto_scale_formula = auto_scale_formula
            pool.enable_auto_scale = True
        else:
            pool.target_dedicated = target_dedicated
            pool.enable_auto_scale = False

        pool.enable_inter_node_communication = enable_inter_node_communication

        if os_family:
            pool.cloud_service_configuration = CloudServiceConfiguration(os_family)
        else:
            if image:
                version = 'latest'
                try:
                    publisher, offer, sku = image.split(':', 2)
                except ValueError:
                    message = ("Incorrect format for VM image URN. Should be in the format: \n"
                               "'publisher:offer:sku[:version]'")
                    raise ValueError(message)
                try:
                    sku, version = sku.split(':', 1)
                except ValueError:
                    pass
                pool.virtual_machine_configuration = VirtualMachineConfiguration(
                    ImageReference(publisher, offer, sku, version),
                    node_agent_sku_id)

        if start_task_command_line:
            pool.start_task = StartTask(start_task_command_line)
            pool.start_task.wait_for_success = start_task_wait_for_success
            pool.start_task.resource_files = start_task_resource_files
        if resize_timeout:
            pool.resize_timeout = resize_timeout

        if metadata:
            pool.metadata = metadata
        if certificate_references:
            pool.certificate_references = certificate_references
        if application_package_references:
            pool.application_package_references = application_package_references

    add_option = PoolAddOptions()
    job_utils._handle_batch_exception(lambda: client.pool.add(pool, add_option))  # pylint: disable=protected-access
    # return client.pool.get(pool.id)


create_pool.__doc__ = PoolAddParameter.__doc__


def create_job(client, account_name=None, account_endpoint=None,  # pylint:disable=too-many-arguments, too-many-locals
               template=None, parameters=None, json_file=None, id=None,  # pylint:disable=redefined-builtin
               pool_id=None, priority=None, uses_task_dependencies=False, metadata=None,
               job_max_wall_clock_time=None, job_max_task_retry_count=None,
               job_manager_task_command_line=None, job_manager_task_environment_settings=None,
               job_manager_task_id=None, job_manager_task_resource_files=None):
    # pylint: disable=too-many-branches, too-many-statements
    if template or json_file:
        working_folder = '.'
        if template:
            logger.warning('You are using an experimental feature {Job Template}.')
            expanded_job_object = template_utils.expand_template(template, parameters)
            if 'job' not in expanded_job_object:
                raise ValueError('Missing job element in the template.')
            if 'properties' not in expanded_job_object['job']:
                raise ValueError('Missing job properties element in the template.')
            # bulid up the jsonFile object to hand to the batch service.
            json_obj = expanded_job_object['job']['properties']
            working_folder = os.path.dirname(template)
        else:
            with open(json_file) as f:
                json_obj = json.load(f)
            # validate the json file
            job = client._deserialize('JobAddParameter', json_obj)  # pylint: disable=protected-access
            if job is None:
                raise ValueError("JSON file '{}' is not in correct format.".format(json_file))
            working_folder = os.path.dirname(json_file)

        if 'applicationTemplateInfo' in json_obj:
            logger.warning('You are using an experimental feature {Application Templates}.')
            json_obj = template_utils.expand_application_template(json_obj, working_folder)

        auto_complete = False
        task_collection = []
        file_utils = FileUtils(None, account_name, None, account_endpoint)
        if 'taskFactory' in json_obj:
            logger.warning('You are using an experimental feature {Task Factory}.')
            task_collection = template_utils.expand_task_factory(json_obj, file_utils)

            # If job has a task factory and terminate job on all tasks complete is set, the job will
            # already be terminated when we add the tasks, so we need to set to noAction, then patch
            # the job once the tasks have been submitted.
            if 'onAllTasksComplete' in json_obj and json_obj['onAllTasksComplete'] != 'noaction':
                auto_complete = json_obj['onAllTasksComplete']
                json_obj['onAllTasksComplete'] = 'noaction'

        should_get_pool = template_utils.should_get_pool(task_collection)
        pool_os_flavor = None
        if should_get_pool:
            pool = job_utils.get_target_pool(client, json_obj)
            pool_os_flavor = pool_utils.get_pool_target_os_type(pool)

        # Handle package management on autopool
        if 'poolInfo' in json_obj and 'autoPoolSpecification' in json_obj['poolInfo'] \
                and 'pool' in json_obj['poolInfo']['autoPoolSpecification'] \
                and 'packageReferences' in json_obj['poolInfo']['autoPoolSpecification']['pool']:

            logger.warning('You are using an experimental feature {Package Management}.')
            pool = json_obj['poolInfo']['autoPoolSpecification']['pool']
            cmds = [template_utils.process_pool_package_references(pool)]
            pool_os_flavor = pool_utils.get_pool_target_os_type(pool)
            pool['startTask'] = template_utils.construct_setup_task(
                pool.get('startTask'), cmds, pool_os_flavor)

        commands = []
        # Handle package management on tasks
        commands.append(template_utils.process_task_package_references(
            task_collection, pool_os_flavor))

        # Handle any special post-processing steps.
        # - Application templates
        # - Resource Files
        # - Output Files
        # - etc
        json_obj = template_utils.post_processing(json_obj, file_utils)
        if task_collection:
            task_collection = template_utils.post_processing(task_collection, file_utils)

        commands.append(template_utils.process_job_for_output_files(
            json_obj, task_collection, pool_os_flavor, file_utils))
        json_obj['jobPreparationTask'] = template_utils.construct_setup_task(
            json_obj.get('jobPreparationTask'), commands, pool_os_flavor)

        # Batch Shipyard integration
        if any(t.get('clientExtensions', {}).get('dockerOptions') for t in task_collection):
            logger.warning('You are using an experimental feature'
                           ' {Job and task creation with Batch Shipyard}.')
            # batchShipyardUtils.createJobAndAddTasks(
            #       parsedJson, taskCollection, pool, options, cli, _);
            # return

        # We deal all NCJ work with pool, now convert back to original type
        job = client._deserialize('JobAddParameter', json_obj)  # pylint:disable=W0212

    else:
        if not id:
            raise ValueError('Need either template, json_file, or id')

        pool = PoolInformation(pool_id=pool_id)
        job = JobAddParameter(id, pool, priority=priority)
        job.uses_task_dependencies = uses_task_dependencies
        if job_max_wall_clock_time is not None or job_max_task_retry_count is not None:
            constraints = JobConstraints(max_wall_clock_time=job_max_wall_clock_time,
                                         max_task_retry_count=job_max_task_retry_count)
            job.constraints = constraints

        if metadata:
            job.metadata = metadata

        if job_manager_task_command_line and job_manager_task_id:
            job_manager_task = JobManagerTask(job_manager_task_id,
                                              job_manager_task_command_line,
                                              resource_files=job_manager_task_resource_files,
                                              environment_settings=job_manager_task_environment_settings)  # pylint: disable=line-too-long
            job.job_manager_task = job_manager_task

    def add_job_and_tasks():
        add_option = JobAddOptions()
        client.job.add(job, add_option)

        if task_collection:
            job_utils.deploy_tasks(client, job.id, task_collection)
            if auto_complete:
                # If the option to terminate the job was set, we need to reapply it with a patch
                # now that the tasks have been added.
                client.job.patch(job.id, {'on_all_tasks_complete': auto_complete})

        # return client.job.get(job.id)

    return job_utils._handle_batch_exception(add_job_and_tasks)  # pylint: disable=protected-access


create_job.__doc__ = JobAddParameter.__doc__ + "\n" + JobConstraints.__doc__


def upload_file(client, local_path, file_group,  # pylint: disable=too-many-arguments
                resource_group=None, account_name=None, remote_path=None, flatten=None):
    """Upload local file or directory of files to storage"""
    file_utils = FileUtils(client, account_name, resource_group, None)
    blob_client = file_utils.resolve_storage_account()
    path, files = resolve_file_paths(local_path)
    if len(files) > 0:
        for f in files:
            file_name = os.path.relpath(f, path)
            upload_blob(f, file_group, file_name, blob_client,
                        remote_path=remote_path, flatten=flatten)
    else:
        raise ValueError('No files or directories found matching local path {}'.format(local_path))


def download_file(client, local_path, file_group,  # pylint: disable=too-many-arguments
                  resource_group=None, account_name=None, remote_path=None, overwrite=False):
    """Download auto-storage file or directory of files to local"""
    file_utils = FileUtils(client, account_name, resource_group, None)
    blob_client = file_utils.resolve_storage_account()
    if remote_path and not remote_path.endswith('/'):
        remote_path += '/'
    files = resolve_remote_paths(blob_client, file_group, remote_path)
    if len(files) > 0:
        for f in files:
            file_name = os.path.realpath(\
                os.path.join(local_path, f.name[len(remote_path):] if remote_path else f.name))
            if not os.path.exists(file_name) or overwrite:
                if not os.path.exists(os.path.dirname(file_name)):
                    try:
                        os.makedirs(os.path.dirname(file_name))
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                download_blob(f.name, file_group, file_name, blob_client)
    else:
        raise ValueError('No files found matching remote path {}'.format(remote_path))
