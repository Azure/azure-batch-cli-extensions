# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import json
import time
import sys
import datetime

from azure.common.credentials import ServicePrincipalCredentials
import azext.batch as batch
from azext.batch import models, operations

OUTPUT_CONTAINER_SAS = ""

BATCH_ENDPOINT = ""
BATCH_ACCOUNT = ""
SUBSCRIPTION_ID = ""
BATCH_CLIENT_ID = ""
BATCH_SECRET = ""
BATCH_TENANT = ""

BATCH_RESOURCE = "https://batch.core.windows.net/"
SAMPLE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    # Authentication.
    # Note that providing credentials and subscription ID is not required
    # if the Azure CLI is installed and already authenticated.
    creds = ServicePrincipalCredentials(
        client_id=BATCH_CLIENT_ID,
        secret=BATCH_SECRET,
        tenant=BATCH_TENANT,
        resource=BATCH_RESOURCE
    )
    
    # Setup client
    client = batch.BatchExtensionsClient(
        credentials=creds,
        base_url=BATCH_ENDPOINT,
        batch_account=BATCH_ACCOUNT,
        subscription_id=SUBSCRIPTION_ID)

    # Setup test input data
    input_data = os.path.join(SAMPLE_DIR, 'ffmpeg', 'data')
    filegroup = 'music-data'
    client.file.upload(input_data, filegroup)

    ## Create pool from template
    pool_template =  os.path.join(SAMPLE_DIR, 'ffmpeg', 'pool.json')
    pool_json = client.pool_extensions.expand_template(pool_template)
    pool_param = operations.ExtendedPoolOperations.poolparameter_from_json(pool_json)
    client.pool.add(pool_param)

    # Create task-per-file job from template file with json parameters
    job_template =  os.path.join(SAMPLE_DIR, 'ffmpeg', 'job.perFile.json')
    parameters = {
        "jobId": {
            "value": "ffmpeg-task-per-file-test"
        },
        "inputFileGroup": {
            "value": filegroup
        },  
        "outputFileStorageUrl": {
            "value": OUTPUT_CONTAINER_SAS
        },
        "poolId": {
            "value": pool_param.properties.id
        }
    }
    job_def = client.job_extensions.expand_template(job_template, parameters)
    job_param = operations.ExtendedJobOperations.jobparameter_from_json(job_def)
    client.job.add(job_param)

    # Create parametric sweep job using models
    job_id = "ffmpeg-parametric-sweep-test"
    task_factory = models.ParametricSweepTaskFactory(
        parameter_sets=[models.ParameterSet(start=1, end=5)],
        repeat_task=models.RepeatTask(
            command_line="ffmpeg -y -i sample{0}.mp3 -acodec libmp3lame output.mp3",
            resource_files=[models.ExtendedResourceFile(source=models.FileSource(file_group=filegroup))],
            output_files=[models.OutputFile(
                file_pattern="output.mp3",
                destination=models.ExtendedOutputFileDestination(
                    auto_storage=models.OutputFileAutoStorageDestination(job_id, path="audio{0}.mp3")),
                upload_options=models.OutputFileUploadOptions(models.OutputFileUploadCondition.task_success))],
            package_references=[models.AptPackageReference(id="ffmpeg")]))
    job = models.ExtendedJobParameter(
        id=job_id,
        pool_info=models.PoolInformation(pool_id=pool_param.properties.id),
        constraints=models.JobConstraints(
            max_wall_clock_time=datetime.timedelta(hours=5),
            max_task_retry_count=1),
        on_all_tasks_complete = models.OnAllTasksComplete.terminate_job,
        task_factory=task_factory)
    client.job.add(job)

    # Wait for job to complete and download outputs from file group.
    while True:
        time.sleep(15)
        job = client.job.get(job_id)
        print("Watching job: {}".format(job.state))
        if job.state == models.JobState.completed:
            client.file.download(SAMPLE_DIR, job_id)
            break
