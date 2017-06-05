# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import json
import time

import azure.batch_extensions as batch
from azure.batch_extensions import models


BATCH_ENDPOINT = os.environ['AZURE_BATCH_ENDPOINT']
BATCH_ACCOUNT = os.environ['AZURE_BATCH_ACCOUNT']
OUTPUT_CONTAINER_SAS = ""
SAMPLE_DIR = os.path.dirname(os.path.dirname(__file__))

if __name__ == '__main__':
    # Setup client
    client = batch.BatchExtensionsClient(base_url=BATCH_ENDPOINT, batch_account=BATCH_ACCOUNT)
    
    # Setup test render input data
    scene_file = os.path.join(SAMPLE_DIR, 'blender', 'scene.blend')
    blender_data = 'blender-app-template-data'
    client.file.upload(scene_file, blender_data)

    # Create pool using existing pool template file
    pool_id = 'blender-app-template-test-pool'
    path_to_pool = os.path.join(SAMPLE_DIR, 'blender-appTemplate', 'pool.json')
    with open(path_to_pool, 'r') as template:
        pool_json = json.load(template)
    pool_parameters = {'poolId': pool_id}
    pool_json = client.pool.expand_template(pool_json, pool_parameters)
    pool = client.pool.poolparameter_from_json(pool_json)
    try:
        client.pool.add(pool)
    except models.BatchErrorException:
        pass  # Pool already exists

    # Create a pool model with an application template reference
    pool_ref = models.PoolInformation(pool_id=pool_id)
    job_id = 'blender-app-template-test'
    blender_job = models.ExtendedJobParameter(job_id, pool_ref)
    blender_job.display_name = "Blender Render using Application Templates"
    blender_job.on_all_tasks_complete = models.OnAllTasksComplete.terminate_job
    blender_job.application_template_info = models.ApplicationTemplateInfo(
        file_path=os.path.join(SAMPLE_DIR, 'blender-appTemplate', 'render-template.json'),
        parameters={
            "blendFile": os.path.basename(scene_file),
            "sceneData": "blender-app-template-data",
            "frameStart": 1,
            "frameEnd": 10,
            "outputFileStorageUrl": OUTPUT_CONTAINER_SAS,
            "outputPrefix": "blenderjob"}
    )
    client.job.add(blender_job)

    # When job is finished, delete pool
    while True:
        time.sleep(15)
        job = client.job.get(job_id)
        print("Watching job: {}".format(job.state))
        if job.state == models.JobState.completed:
            break

    client.pool.delete(pool_id)