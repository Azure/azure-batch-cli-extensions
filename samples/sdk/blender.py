# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import time

import azure.batch_extensions as batch
from azure.batch_extensions import models


BATCH_ENDPOINT = os.environ['AZURE_BATCH_ENDPOINT']
BATCH_ACCOUNT = os.environ['AZURE_BATCH_ACCOUNT']
SAMPLE_DIR = os.path.dirname(os.path.dirname(__file__))

if __name__ == '__main__':

    # Set up client
    client = batch.BatchExtensionsClient(base_url=BATCH_ENDPOINT, batch_account=BATCH_ACCOUNT)

    # Upload inputs
    input_file = os.path.join(SAMPLE_DIR, "blender", "scene.blend")
    client.file.upload(input_file, "blender-data")

    # Load template file and parameters
    path_to_template = os.path.join(SAMPLE_DIR, "blender", "render.json")
    path_to_parameters = os.path.join(SAMPLE_DIR, "blender", "parameters.json")
    job_json = client.job.expand_template(path_to_template, path_to_parameters)

    # Create job
    job = client.job.jobparameter_from_json(job_json)
    job_id = job.id
    client.job.add(job)

    # Wait for job to complete and download outputs from file group.
    while True:
        time.sleep(15)
        job = client.job.get(job_id)
        print("Watching job: {}".format(job.state))
        if job.state == models.JobState.completed:
            client.file.download('blender-outputs', job_id)
            break

    # Delete job
    client.job.delete(job_id)