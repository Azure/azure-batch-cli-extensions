# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import multiprocessing

from azext.batch.models import PoolAddParameter, JobAddParameter, JobConstraints
from azext.batch.errors import CreateTasksErrorException
from azure.cli.core.util import get_file_json

from knack.log import get_logger
from knack.prompting import prompt

logger = get_logger(__name__)

# NCJ custom commands
# pylint: disable=redefined-builtin


def create_pool(client, template=None, parameters=None, json_file=None, id=None, vm_size=None,  # pylint:disable=too-many-arguments, too-many-locals
                target_dedicated_nodes=None, target_low_priority_nodes=None, auto_scale_formula=None,  # pylint: disable=redefined-builtin
                enable_inter_node_communication=False, os_family=None, image=None,
                node_agent_sku_id=None, resize_timeout=None, start_task_command_line=None,
                start_task_resource_files=None, start_task_wait_for_success=False, application_licenses=None,
                certificate_references=None, application_package_references=None, metadata=None):
    # pylint: disable=too-many-branches, too-many-statements
    from azext.batch.errors import MissingParameterValue
    from azext.batch.models import (
        PoolAddOptions, StartTask, ImageReference,
        CloudServiceConfiguration, VirtualMachineConfiguration)
    if template or json_file:
        if template:
            json_obj = None
            parameters = get_file_json(parameters) if parameters else {}
            template_obj = get_file_json(template)
            while json_obj is None:
                try:
                    json_obj = client.pool.expand_template(template_obj, parameters)
                except MissingParameterValue as error:
                    param_prompt = error.parameter_name
                    param_prompt += " ({}): ".format(error.parameter_description)
                    parameters[error.parameter_name] = prompt(param_prompt)
                except TypeError as error:
                    raise ValueError(str(error))
                else:
                    json_obj = json_obj.get('properties', json_obj)
        else:
            json_obj = get_file_json(json_file)
        # validate the json file
        pool = client.pool.poolparameter_from_json(json_obj)
        if pool is None:
            raise ValueError("JSON pool parameter is not in correct format.")
    else:
        if not id:
            raise ValueError('Please supply template, json_file, or id')

        pool = PoolAddParameter(id, vm_size=vm_size)
        if auto_scale_formula:
            pool.auto_scale_formula = auto_scale_formula
            pool.enable_auto_scale = True
        else:
            pool.target_dedicated_nodes = target_dedicated_nodes
            pool.target_low_priority_nodes = target_low_priority_nodes
            pool.enable_auto_scale = False

        pool.enable_inter_node_communication = enable_inter_node_communication

        if os_family:
            pool.cloud_service_configuration = CloudServiceConfiguration(os_family)
        else:
            if image:
                version = 'latest'
                try:
                    publisher, offer, sku = image.split(':', 2)
                    try:
                        sku, version = sku.split(':', 1)
                    except ValueError:
                        pass
                    pool.virtual_machine_configuration = VirtualMachineConfiguration(
                        image_reference=ImageReference(publisher=publisher, offer=offer, sku=sku, version=version),
                        node_agent_sku_id=node_agent_sku_id)
                except ValueError:
                    if '/' not in image:
                        message = ("Incorrect format for VM image. Should be in the format: \n"
                                   "'publisher:offer:sku[:version]' OR a URL to an ARM image.")
                        raise ValueError(message)
                    pool.virtual_machine_configuration = VirtualMachineConfiguration(
                        image_reference=ImageReference(virtual_machine_image_id=image),
                        node_agent_sku_id=node_agent_sku_id)

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
        if application_licenses:
            pool.application_licenses = application_licenses
        if application_package_references:
            pool.application_package_references = application_package_references

    add_option = PoolAddOptions()
    client.pool.add(pool, add_option)


create_pool.__doc__ = PoolAddParameter.__doc__


def create_job(client, template=None, parameters=None, json_file=None, id=None,  # pylint:disable=too-many-arguments, too-many-locals
               pool_id=None, priority=None, uses_task_dependencies=False, metadata=None,
               job_max_wall_clock_time=None, job_max_task_retry_count=None,
               job_manager_task_command_line=None, job_manager_task_environment_settings=None,
               job_manager_task_id=None, job_manager_task_resource_files=None):
    # pylint: disable=too-many-branches, too-many-statements
    from azext.batch.errors import MissingParameterValue
    from azext.batch.models import JobManagerTask, JobAddOptions, PoolInformation
    if template or json_file:
        if template:
            json_obj = None
            parameters = get_file_json(parameters) if parameters else {}
            template_obj = get_file_json(template)
            while json_obj is None:
                try:
                    json_obj = client.job.expand_template(template_obj, parameters)
                except MissingParameterValue as error:
                    param_prompt = error.parameter_name
                    param_prompt += " ({}): ".format(error.parameter_description)
                    parameters[error.parameter_name] = prompt(param_prompt)
                except TypeError as error:
                    raise ValueError(str(error))
                else:
                    json_obj = json_obj.get('properties', json_obj)
        else:
            json_obj = get_file_json(json_file)
        # validate the json file
        job = client.job.jobparameter_from_json(json_obj)
        if job is None:
            raise ValueError("JSON job parameter is not in correct format.")
    else:
        if not id:
            raise ValueError('Please supply template, json_file, or id')

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

    add_option = JobAddOptions()
    try:
        client.job.add(job, add_option, threads=multiprocessing.cpu_count()/2)
    except CreateTasksErrorException as e:
        for error in e.failures:
            logger.warning(error.task_id + " failed to be added due to " + error.error.code)

create_job.__doc__ = JobAddParameter.__doc__ + "\n" + JobConstraints.__doc__


def upload_file(client, local_path, file_group,  # pylint: disable=too-many-arguments
                remote_path=None, flatten=None):
    """Upload local file or directory of files to storage"""
    client.file.upload(local_path, file_group, remote_path=remote_path, flatten=flatten)


def download_file(client, local_path, file_group,  # pylint: disable=too-many-arguments
                  remote_path=None, overwrite=False):
    """Download auto-storage file or directory of files to local"""
    client.file.download(local_path, file_group, remote_path=remote_path, overwrite=overwrite)
