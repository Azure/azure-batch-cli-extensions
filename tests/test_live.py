# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import tempfile
import json
import datetime

from azext.batch.models import BatchErrorException, AllocationState, ComputeNodeState, TaskState, VerificationType
import azure.batch.batch_auth as batchauth
import azext.batch as batch
from tests.vcr_test_base import VCRTestBase
from azure.common import AzureMissingResourceHttpError
from azure.multiapi.storage.v2018_11_09.common import CloudStorageAccount
from azure.multiapi.storage.v2018_11_09.blob import BlobPermissions

class TestFileUpload(VCRTestBase):
    def __init__(self, test_method):
        super(TestFileUpload, self).__init__(__file__, test_method)
        if self.playback:
            self.account_name = 'sdktest2'
            self.resource_name = 'sdktest'
            self.account_endpoint = 'https://sdktest2.westcentralus.batch.azure.com'
        else:
            self.account_name = os.environ.get('AZURE_BATCH_ACCOUNT', 'test1')
            self.resource_name = os.environ.get('AZURE_BATCH_RESOURCE_GROUP', 'test_rg')
            self.account_endpoint = os.environ.get('AZURE_BATCH_ENDPOINT', 'https://test1.westus.batch.azure.com/')
        self.testPrefix = 'cli-batch-extensions-live-tests'

    def cmd(self, command, checks=None, allowed_exceptions=None,
            debug=False):
        command = '{} --resource-group {} --account-name {} --account-endpoint {}'.format(
            command,
            self.resource_name,
            self.account_name,
            self.account_endpoint)
        return super(TestFileUpload, self).cmd(command=command, checks=checks,
                                               allowed_exceptions=allowed_exceptions, debug=debug)

    def test_batch_upload_live(self):
        self.execute()

    def body(self):
        # should upload a local file to auto-storage
        input_str = os.path.join(os.path.dirname(__file__), 'data', 'file_tests', 'foo.txt')
        result = self.cmd(command=r'batch file upload --local-path "{}" --file-group {}'.
                          format(input_str, self.testPrefix))
        print('Result text:{}'.format(result))

        # should upload a local file to auto-storage with path prefix
        result = self.cmd(command=r'batch file upload --local-path "{}" --file-group {} '
                          '--remote-path "test/data"'.format(input_str, self.testPrefix))
        print('Result text:{}'.format(result))


class TestBatchExtensionsLive(VCRTestBase):
    # pylint: disable=attribute-defined-outside-init,no-member
    def __init__(self, test_method):
        super(TestBatchExtensionsLive, self).__init__(__file__, test_method)
        if self.playback:
            self.account_name = 'sdktest2'
            self.account_endpoint = 'https://sdktest2.westcentralus.batch.azure.com'
            self.account_key = 'abc=='
            self.subscription_id = "677f962b-9abf-4423-a27b-0c2f4094dcec"
            storage_account = 'sdkteststore2'
            storage_key = 'abc=='
        else:
            self.account_name = os.environ.get('AZURE_BATCH_ACCOUNT', 'test1')
            self.account_endpoint = os.environ.get('AZURE_BATCH_ENDPOINT', 'https://test1.westus.batch.azure.com/')
            self.account_key = os.environ['AZURE_BATCH_ACCESS_KEY']
            self.subscription_id = os.environ.get(
                'AZURE_BATCH_SUBSCRIPTION_ID',
                "677f962b-9abf-4423-a27b-0c2f4094dcec")
            storage_account = os.environ.get('AZURE_STORAGE_ACCOUNT', 'testaccountforbatch')
            storage_key = os.environ.get('AZURE_STORAGE_ACCESS_KEY', 'abc==')

        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.blob_client = CloudStorageAccount(storage_account, storage_key)\
            .create_block_blob_service()
        credentials = batchauth.SharedKeyCredentials(self.account_name, self.account_key)
        self.batch_client = batch.BatchExtensionsClient(
            credentials,
            batch_url=self.account_endpoint,
            subscription_id=self.subscription_id,
            batch_account=self.account_name)

        self.output_blob_container = 'aaatestcontainer'
        sas_token = self.blob_client.generate_container_shared_access_signature(
            container_name=self.output_blob_container,
            permission=BlobPermissions(read=True, write=True),
            start=datetime.datetime.utcnow(),
            expiry=datetime.datetime.utcnow() + datetime.timedelta(days=1))
        self.output_container_sas = 'https://{}.blob.core.windows.net/{}?{}'.format(
            storage_account,
            self.output_blob_container,
            sas_token)
        print('Full container sas: {}'.format(self.output_container_sas))

    def cmd(self, command, checks=None, allowed_exceptions=None,
            debug=False):
        command = r'{} --account-name {} --account-key "{}" --account-endpoint {}'.format(
            command,
            self.account_name,
            self.account_key,
            self.account_endpoint)
        return super(TestBatchExtensionsLive, self).cmd(command, checks, allowed_exceptions, debug)

    def test_batch_extensions_live(self):
        self.execute()

    def submit_job_wrapper(self, file_name):
        try:
            result = self.cmd(r'batch job create --template "{}"'.format(file_name))
        except Exception as exp:
            result = exp
        print('Result text:{}'.format(result))

    def wait_for_tasks_complete(self, job_id, timeout):
        print('waiting for tasks to be complete')

        while True:
            tasks = list(self.batch_client.task.list(job_id))
            # Determine if the tasks are in completed state
            all_completed = True
            print('determining if {} tasks are complete'.format(len(tasks)))
            for task in tasks:
                if task.state != TaskState.completed:
                    print('state is {}'.format(task.state))
                    all_completed = False
            if all_completed:
                print('Tasks in job {} are now completed.'.format(job_id))
                return
            wait_for = 3
            timeout = timeout - wait_for
            if timeout < 0:
                raise RuntimeError('Timed out')
            else:
                import time
                time.sleep(wait_for)

    def wait_for_pool_steady(self, pool_id, timeout):
        print('waiting for pool to reach steady state')

        while True:
            pool = self.batch_client.pool.get(pool_id)
            if pool.allocation_state == AllocationState.steady:
                print('pool reached steady state')
                return
            else:
                wait_for = 3
                timeout = timeout - wait_for
                if timeout < 0:
                    raise RuntimeError('Timed out')
                else:
                    import time
                    time.sleep(wait_for)

    def wait_for_vms_idle(self, pool_id, timeout):
        print('waiting for vms to be idle')

        while True:
            nodes = self.batch_client.compute_node.list(pool_id)
            # Determine if the nodes are in the idle state
            all_idle = True
            for node in nodes:
                if node.state != ComputeNodeState.idle:
                    all_idle = False
            if all_idle:
                print('VMs in pool {} are now idle.'.format(pool_id))
                return
            else:
                wait_for = 3
                timeout = timeout - wait_for
                if timeout < 0:
                    raise RuntimeError('Timed out')
                else:
                    import time
                    time.sleep(wait_for)

    def clear_container(self, container_name):
        try:
            print('clearing container {}'.format(container_name))
            blobs = self.blob_client.list_blobs(container_name)
            blobs = [b.name for b in blobs]
            for blob in blobs:
                self.blob_client.delete_blob(container_name, blob)
        except AzureMissingResourceHttpError:
            pass

    def create_basic_spec(self, job_id, pool_id, task_id, text, is_windows):  # pylint: disable=too-many-arguments
        cmd_line = None
        if is_windows:
            # Strip pesky newline from echo
            cmd_line = 'cmd /c echo | set /p dummy={}'.format(text)
        else:
            cmd_line = '/bin/bash -c "echo {}"'.format(text)
        return {
            'job': {
                'type': 'Microsoft.Batch/batchAccounts/jobs',
                'apiVersion': '2018-12-01',
                'properties': {
                    'id': job_id,
                    'poolInfo': {
                        'poolId': pool_id
                    },
                    'taskFactory': {
                        'type': 'taskCollection',
                        'tasks': [
                            {
                                'id': task_id,
                                'commandLine': cmd_line,
                                'constraints': {
                                    'retentionTime': "PT1H"
                                },
                                'outputFiles': [
                                    {
                                        'filePattern': '$AZ_BATCH_TASK_DIR/*.txt',
                                        'destination': {
                                            'container': {
                                                'containerUrl': self.output_container_sas
                                            }
                                        },
                                        'uploadOptions': {
                                            'uploadCondition': 'TaskSuccess'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

    def create_basic_spec_alt(self, job_id, pool_id, task_id, text, is_windows):  # pylint: disable=too-many-arguments
        cmd_line = None
        if is_windows:
            # Strip pesky newline from echo
            cmd_line = 'cmd /c echo | set /p dummy={}'.format(text)
        else:
            cmd_line = '/bin/bash -c "echo {}"'.format(text)
        return {
            'job': {
                'type': 'Microsoft.Batch/batchAccounts/jobs',
                'apiVersion': '2018-12-01',
                'properties': {
                    'id': job_id,
                    'poolInfo': {
                        'poolId': pool_id
                    },
                    'taskFactory': {
                        'type': 'taskCollection',
                        'tasks': [
                            {
                                'id': task_id,
                                'commandLine': cmd_line,
                                'constraints': {
                                    'retentionTime': "PT1H"
                                },
                                'outputFiles': [
                                    {
                                        'filePattern': '$AZ_BATCH_TASK_DIR/*.txt',
                                        'destination': {
                                            'autoStorage': {
                                                'fileGroup': 'output'
                                            }
                                        },
                                        'uploadOptions': {
                                            'uploadCondition': 'TaskSuccess'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

    def create_pool_if_not_exist(self, pool_id, flavor):
        print('Creating pool: {}'.format(pool_id))
        sku_results = self.batch_client.account.list_supported_images()

        publisher = None
        offer = None
        sku_id = None
        node_agent_sku_id = None

        def sku_filter_function(skus):
            for sku in skus:
                if (sku.verification_type == VerificationType.verified and
                        sku.image_reference.publisher == publisher and
                        sku.image_reference.offer == offer and
                        sku.image_reference.sku == sku_id):
                    return sku.node_agent_sku_id
            return None

        if flavor == 'ubuntu16':
            publisher = 'canonical'
            offer = 'ubuntuserver'
            sku_id = '18.04-lts'
        elif flavor == 'centos':
            publisher = 'openlogic'
            offer = 'centos'
            sku_id = '7.0'
        elif flavor == 'debian':
            publisher = 'credativ'
            offer = 'debian'
            sku_id = '8'
        elif flavor == 'windows-2012':
            publisher = 'microsoftwindowsserver'
            offer = 'windowsserver'
            sku_id = '2012-datacenter'
        elif flavor == 'windows-2012-r2':
            publisher = 'microsoftwindowsserver'
            offer = 'windowsserver'
            sku_id = '2012-r2-datacenter'
        elif flavor == 'windows-2016':
            publisher = 'microsoftwindowsserver'
            offer = 'windowsserver'
            sku_id = '2016-datacenter'
        node_agent_sku_id = sku_filter_function(sku_results)

        is_windows = True if publisher.lower() == 'microsoftwindowsserver' else False
        print('Allocating pool {}, {}, {} with agent {}'.
              format(publisher, offer, sku_id, node_agent_sku_id))

        pool = {
            'id': pool_id,
            'vmSize': 'STANDARD_D1_V2',
            'virtualMachineConfiguration': {
                'imageReference': {
                    'publisher': publisher,
                    'offer': offer,
                    'sku': sku_id
                },
                'nodeAgentSKUId': node_agent_sku_id
            },
            'targetDedicatedNodes': 1
        }

        try:
            add_pool = self.batch_client._deserialize('PoolAddParameter', pool)  # pylint:disable=protected-access
            self.batch_client.pool.add(add_pool)
            print('Successfully created pool {}'.format(pool_id))
        except BatchErrorException as ex:
            if ex.error.code == 'PoolExists':
                print('Pool already exists')
            else:
                raise ex

        self.wait_for_pool_steady(pool_id, 5 * 60)
        self.wait_for_vms_idle(pool_id, 5 * 60)
        return is_windows

    def file_upload_helper(self, job_id, pool_id, task_id, pool_flavor,
                           using_file_group):
        is_windows = self.create_pool_if_not_exist(pool_id, pool_flavor)
        text = 'test'
        spec = self.create_basic_spec_alt(job_id, pool_id, task_id, text, is_windows) \
                if using_file_group else \
                self.create_basic_spec(job_id, pool_id, task_id, text, is_windows)

        file_name = os.path.join(tempfile.mkdtemp(), 'uploadTest.json')
        fs = open(file_name, "w")
        fs.write(json.dumps(spec))
        fs.close()

        try:
            result = self.submit_job_wrapper(file_name)
            print(result)
            # result.exitStatus.should.equal(0);

            job = self.batch_client.job.get(job_id)
            self.assertEqual(job.id, job_id)

            self.wait_for_tasks_complete(job_id, 120)
            task = self.batch_client.task.get(job_id, task_id)
            print(task.state)
            self.assertIsNotNone(task.execution_info)
            self.assertIsNone(task.execution_info.failure_info)
            self.assertEqual(task.execution_info.exit_code, 0)

            container_name = 'fgrp-output' if using_file_group else self.output_blob_container
            blobs = self.blob_client.list_blobs(container_name)
            blob_names = [x.name for x in blobs]
            self.assertIn('stdout.txt', blob_names)
            self.assertIn('stderr.txt', blob_names)
            self.assertIn('fileuploadout.txt', blob_names)
            self.assertIn('fileuploaderr.txt', blob_names)
            stdout_blob = [x for x in blobs if x.name == 'stdout.txt'][0]
            self.assertTrue(stdout_blob.properties.content_length>=4)
        finally:
            print('Deleting job {}'.format(job_id))
            self.batch_client.job.delete(job_id=job_id)

    def body(self):
        # file egress should work on ubuntu 16.04
        self.clear_container(self.output_blob_container)
        job_id = 'ncj-ubuntu1604'
        pool_id = 'ncj-ubuntu1604'
        task_id = 'myTask'
        self.file_upload_helper(job_id, pool_id, task_id, 'ubuntu16', False)

        # should work on Windows 2012 R2
        self.clear_container(self.output_blob_container)
        job_id = 'ncj-windows-2012-r2'
        pool_id = 'ncj-windows-2012-r2'
        task_id = 'myTask'
        self.file_upload_helper(job_id, pool_id, task_id, 'windows-2012-r2', False)

        # file egress should work on ubuntu 16.04
        self.clear_container('fgrp-output')
        job_id = 'ncj-ubuntu1604-1'
        pool_id = 'ncj-ubuntu1604'
        task_id = 'myTask'
        self.file_upload_helper(job_id, pool_id, task_id, 'ubuntu16', True)

        # should work on Windows 2012 R2
        self.clear_container('fgrp-output')
        job_id = 'ncj-windows-2012-r2-1'
        pool_id = 'ncj-windows-2012-r2'
        task_id = 'myTask'
        self.file_upload_helper(job_id, pool_id, task_id, 'windows-2012-r2', True)

        # Batch Explorer workflow
        with open(os.path.join(self.data_dir, 'batch.pool.simple.resourcefile-legacy.json'), 'r') as template:
            json_obj = json.load(template)
        expanded_template = self.batch_client.pool.expand_template(json_obj)
        pool_param = self.batch_client.pool.poolparameter_from_json(expanded_template)
        self.batch_client.pool.add(pool_param)
        self.wait_for_pool_steady(pool_param.id, 5 * 60)
        self.batch_client.pool.delete(pool_param.id)

        # Batch simple legacy task factory
        self.cmd("batch job create --template '{}'".format(os.path.join(
            self.data_dir,
            'batch.job.resourcefile-legacy.json')))

        # Merge Task
        self.cmd("batch file upload --file-group 'in' --local-path '{}'".format(self.data_dir))
        self.cmd("batch job create --template '{}'".format(os.path.join(
            self.data_dir,
            'batch.job.mergetask.json')))
