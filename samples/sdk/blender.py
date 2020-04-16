# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import time

from azure.common.credentials import ServicePrincipalCredentials
import azext.batch as batch
from azext.batch import models, operations


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
    
    # Set up client
    client = batch.BatchExtensionsClient(
        credentials=creds,
        base_url=BATCH_ENDPOINT,
        batch_account=BATCH_ACCOUNT,
        subscription_id=SUBSCRIPTION_ID)

    # Upload inputs
    input_file = os.path.join(SAMPLE_DIR, "blender", "scene.blend")
    client.file.upload(input_file, "blender-data")

    # Load template file and parameters
    path_to_template = os.path.join(SAMPLE_DIR, "blender", "render.json")
    path_to_parameters = os.path.join(SAMPLE_DIR, "blender", "parameters.json")
    job_json = client.job_extensions.expand_template(path_to_template, path_to_parameters)

    # Create job
    job = operations.ExtendedJobOperations.jobparameter_from_json(job_json)
    job_id = job.properties.id
    client.job.add(job)

    # Wait for job to complete and download outputs from file group.
    while True:
        time.sleep(15)
        job = client.job.get(job_id)
        print("Watching job: {}".format(job.state))
        if job.state == models.JobState.completed:
            client.file.download(SAMPLE_DIR, 'blender-outputs')
            break

    # Delete job
    client.job.delete(job_id)

    # Delete input and output data
    client.file.delete_group('blender-data')
    client.file.delete_group('blender-outputs')
