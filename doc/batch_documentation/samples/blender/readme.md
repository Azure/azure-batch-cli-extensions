# Azure Batch Blender

This sample shows how to use **Blender** to render using a parameterized template that specifies a virtualMachineConfiguration based autopool.

## Features used by this sample

* [Job template with parameterization](../../templates.md)
* [Parametric sweep task factory](../../taskFactories.md#parametric-sweep)
* [Automatic persistence of task output files to Azure Storage](../../outputFiles.md)

## Prerequisites

You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

You will need a Blender scene to render.

## Upload files

To upload your blender files:

```bash
azure batch file upload <path> blender-data
```

Run this command on a folder containing the blender files you want to process. `blender-data` is the default value of the `sceneData` parameter in the job template. If you upload your files to a different file group, be sure to provide this value for the `sceneData` parameter when creating your job (see the next section).

## Create the job

Modify the `parameters.json` file to specify appropriate parameters for the job. The full set of available parameters is defined in `render.json`:

| Parameter            | Required  | Description                                                                                 |
| -------------------- | --------- | ------------------------------------------------------------------------------------------- |
| blendFile            | Mandatory | File name of the Blender scene to be rendered                                               |
| sceneData            | Optional  | Name of the file group where the input data is stored. <br/> Defaults to `blender-data`.    |
| numberNodes          | Optional  | Number of nodes in the Azure Batch pool where the job will run. <br/> Defaults to `5`.      |
| vmSize               | Optional  | Size of the virtual machines that run the application. <br/> Defaults to `STANDARD_A1`.     |
| jobName              | Mandatory | Prefix of the name of the Azure Batch job, also used to prefix rendered outputs.            |
| frameStart           | Mandatory | Index of the first frame to render.                                                         |
| frameEnd             | Mandatory | Index of the last frame to render.                                                          |
| outputFileStorageUrl | Mandatory | SAS URL for a container where outputs will be stored.                                       |

When you are ready to run the job, use this command:

```bash
azure batch job create --template render.json --parameters parameters.json
```

This job uses an **autopool** which will automatically be deleted once the job reaches the Completed state. If the job never reaches the Completed state (e.g. when tasks are unable to run because of scheduling errors, or errors downloading files from storage), you will continue to be charged for the pool. In this case, you may want to use the [Azure portal](https://portal.azure.com) to manually delete the pool to ensure you're not billed unnecessarily.

## Monitor the job

You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample

| File              | Content                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `render.json`     | Specifies the job to run, including a parametric sweep task factory, the autopool definition, parameter and variable definitions. |
| `parameters.json` | Provides parameter values used to create the actual job that will run.                                                            |

