# Azure Batch Blender using application templates

This template shows how to use **Blender** to render using an *application template* to separate the logic of processing from administration and management.

With an *application template*, the processing steps required for the job are defined in a separate file - see `render-template.json` which is appropriately parameterized. The job itself references the template, supplies any required parameter values and specifies the pool on which the job is to run.

## Features used by this sample

* [Split job configuration and management with reusable application templates](../../application-templates.md)
* [Parametric sweep task factory](../../taskFactories.md#parametric-sweep)
* [Automatic persistence of task output files to Azure Storage](../../outputFiles.md)

## Prerequisites

You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

You will need a Blender scene to render.

## Setup Pool

The sample specifies an Azure Batch Pool with the id `blender-pool` - if you don't already have one, run this command:

```bash
azure batch pool create --template pool.json
```
The default settings in `pool.json` specify a pool named `blender-pool` containing **3** **STANDARD_D1** virtual machines.

**You are billed for your Azure Batch pools, so don't forget to delete this pool through the [Azure portal](https://portal.azure.com) when you're done.** 

If you want to use an existing pool to run the job, modify the `render-job.json` file to specify the unique id of your pool.

## Upload files

To upload your blender files:

```bash
azure batch file upload <path> blender-data
```

Run this command on a folder containing the blender files you want to process. `blender-data` is the default value of the `sceneData` parameter in the job template. If you upload your files to a different file group, be sure to provide this value for the `sceneData` parameter when creating your job (see the next section).

## Create the job

Edit the `render-job.json` file to specify appropriate parameters for the job:

| Parameter            | Description                                              |
| -------------------- | -------------------------------------------------------- |
| blendFile            | The Blender scene file to be rendered                    |
| sceneData            | The file group where the input data is stored            |
| outputPrefix         | The prefix to use when naming the rendered outputs       |
| frameStart           | Index of the first frame to render                       |
| frameEnd             | Index of the last frame to render                        |
| outputFileStorageUrl | The SAS URL for a container where outputs will be stored |

When you are ready to run the job, use this command:

```bash
azure batch job create --json-file render-job.json
```

## Monitor the job

You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample

| File                   | Content                                                                                                                                                                                                                                                                                                |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `render-job.json`      | Specifies the job to run, including the pool to use and any runtime constraints. <br/> Does not contain any of the job logic - instead it has an `applicationTemplateInfo` element that specifies the template to use (see `filePath`) and any parameters required by the template (see `parameters`). |
| `render-template.json` | Template file describing the required processing, making use of the experimental **taskFactory** feature.                                                                                                                                                                                              |


