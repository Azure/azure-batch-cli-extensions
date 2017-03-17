# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.exceptions import ValidationError, ClientRequestError
from azure.batch.models import BatchErrorException
from azure.cli.core._util import CLIError

# pylint: disable=too-few-public-methods


def _handle_batch_exception(action):
    try:
        return action()
    except BatchErrorException as ex:
        try:
            message = ex.error.message.value
            if ex.error.values:
                for detail in ex.error.values:
                    message += "\n{}: {}".format(detail.key, detail.value)
            raise CLIError(message)
        except AttributeError:
            raise CLIError(ex)
    except (ValidationError, ClientRequestError) as ex:
        raise CLIError(ex)


def deploy_tasks(client, job_id, tasks):
    MAX_TASKS_COUNT_IN_BATCH = 100

    def add_task():
        start = 0
        while start < len(tasks):
            end = min(start + MAX_TASKS_COUNT_IN_BATCH, len(tasks))
            ts = client._deserialize('[TaskAddParameter]', tasks[start:end])  # pylint: disable=protected-access
            client.task.add_collection(job_id, ts)
            start = end

    _handle_batch_exception(add_task)


def get_task_counts(client, job_id):
    task_counts = {
        'active': 0,
        'running': 0,
        'completed': 0
    }

    def action():
        result = client.task.list(job_id, select='id, state')
        for task in result:
            if task.state in ['active', 'running', 'completed']:
                task_counts[task.state] += 1
            else:
                raise ValueError('Invalid task state')
        return task_counts

    return _handle_batch_exception(action)


def get_target_pool(client, job):
    def action():
        pool_result = client.pool.get(job['poolInfo']['poolId'])
        return client._serialize.body(pool_result, 'CloudPool')  # pylint: disable=protected-access

    if not job.get('poolInfo'):
        raise ValueError('Missing required poolInfo.')

    pool = None
    if 'poolId' in job['poolInfo']:
        pool = _handle_batch_exception(action)
    elif 'autoPoolSpecification' in job['poolInfo'] \
            and job['poolInfo']['autoPoolSpecification'].get('pool'):
        pool = job['poolInfo']['autoPoolSpecification']['pool']
    else:
        raise ValueError('Missing required poolId or autoPoolSpecification.pool.')

    return pool
