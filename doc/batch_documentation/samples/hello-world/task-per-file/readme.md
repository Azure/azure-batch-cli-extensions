# Azure Batch data processing with a task factory

This sample shows how to use a task factory to process a set of files uploaded into storage. The job runs on an VirtualMachineConfiguration based autopool and demonstrates how to use OutputFiles to automatically download/upload files to/from the virtual machine.

## Features used by this sample

* [Input data upload to Batch linked storage accounts](../../../inputFiles.md#input-file-upload)
* [Pool and job templates with parameterization](../../../templates.md)
* [Task per file task factory](../../../taskFactories.md#task-per-file)
* [Automatic persistence of task output files to Azure Storage](../../../outputFiles.md)

## Prerequisites

You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

## Upload files

To upload a folder of files, run this command:
``` bash
azure batch file upload <path> <group>
``` 

`<path>` should point to a folder containing some text files you want to upload for processing. You'll need to quote the path if it contains spaces.

`<group>` is a name to use for these files. You'll use the same group name when configuring your job later on.

## Preparation

Modify `job.parameters.json` to set the parameters for job creation. The following parameters are available:

| Parameter            | Required  | Description                                                                                                     |
| -------------------- | --------- | --------------------------------------------------------------------------------------------------------------- |
| jobId                | Mandatory | The id of the Azure Batch job.                                                                                  |
| poolId               | Optional  | The id of the Azure Batch pool which runs the job. <br/>Defaults to `helloworld-pool` if not specified.         |
| vmSize               | Optional  | The size of the virtual machines that run the application. <br/> Defaults to `STANDARD_D1_V2` if not specified. |
| vmCount              | Optional  | The number of virtual machines in the auto pool. <br/> Defaults to `3` if not specified.                        |
| testData             | Mandatory | The auto-storage group where the input data is stored.                                                          |
| outputFileStorageUrl | Mandatory | A storage SAS URL to a container with write access.                                                             |

If you want to configure other options of the job, such as the pool id, you can look in the `job.json` parameters section to see what options are available.

At minimum, legal values must be provided for all mandatory parameters.

## Run commands

To create your job:
``` bash
azure batch job create --template job.json --parameters job.parameters.json
```

This job uses an **autopool** which will automatically be deleted once the job reaches the Completed state. If the job never reaches the Completed state (e.g. when tasks are unable to run because of scheduling errors, or errors downloading files from storage), you will continue to be charged for the pool. In this case, you may want to use the [Azure portal](https://portal.azure.com) to manually delete the pool to ensure you're not billed unnecessarily.

## Monitor the job

You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample

| File                  | Content                                                                                            |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| `job.json`            | A template for the job to run, including parameter definitions and a **taskPerFile** task factory. |
| `job.parameters.json` | Provides values for the parameters defined in `job.json`.                                          |

