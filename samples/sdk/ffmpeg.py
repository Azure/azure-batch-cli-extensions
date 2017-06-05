# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import json
import time
import sys
import datetime

import azure.batch_extensions as batch
from azure.batch_extensions import models

BATCH_ENDPOINT = os.environ['AZURE_BATCH_ENDPOINT']
BATCH_ACCOUNT = os.environ['AZURE_BATCH_ACCOUNT']
OUTPUT_CONTAINER_SAS = ""
SAMPLE_DIR = os.path.dirname(os.path.dirname(__file__))

if __name__ == '__main__':
    # Setup client
    client = batch.BatchExtensionsClient(base_url=BATCH_ENDPOINT, batch_account=BATCH_ACCOUNT)

    # Setup test input data
    input_data = os.path.join(SAMPLE_DIR, 'ffmpeg', 'data')
    filegroup = 'music-data'
    client.file.upload(input_data, filegroup)

    ## Create pool from template
    pool_template =  os.path.join(SAMPLE_DIR, 'ffmpeg', 'pool.json')
    pool_json = client.pool.expand_template(pool_template)
    pool_param = client.pool.poolparameter_from_json(pool_json)
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
            "value": pool_param.id
        }
    }
    job_def = client.job.expand_template(job_template, parameters)
    job_param = client.job.jobparameter_from_json(job_def)
    client.job.add(job_param)

    # Create parametric sweep job using models
    job_id = "ffmpeg-parametric-sweep-test"
    task_factory = models.ParametricSweepTaskFactory(
        parameter_sets=[models.ParameterSet(1, 5)],
        repeat_task=models.RepeatTask(
            command_line="ffmpeg -y -i sample{0}.mp3 -acodec libmp3lame output.mp3",
            resource_files=[models.ExtendedResourceFile(source=models.FileSource(file_group=filegroup))],
            output_files=[models.TaskOutputFile(
                "output.mp3",
                destination=models.OutputFileDestination(
                    auto_storage=models.AutoStorageDestination(job_id, path="audio{0}.mp3")),
                upload_details=models.OutputFileUploadDetails(models.TaskUploadStatus.task_success))],
            package_references=[models.AptPackageReference("ffmpeg")]))
    job = models.ExtendedJobParameter(
        id=job_id,
        pool_info=models.PoolInformation(pool_id=pool_param.id),
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
            client.file.download(input_data, job_id)
            break
