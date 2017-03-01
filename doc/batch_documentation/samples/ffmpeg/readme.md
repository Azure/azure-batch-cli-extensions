# Azure Batch FFMpeg Pool/Job Template

This sample shows how to use `ffmpeg` to convert one kind of media file (`WAV`) to another type media file (`MP3`). Two approaches are shown, one using a *parametric sweep task factory* and one using a *task per file task factory*.


## Features used by this sample

* [Job template with parameterization](../../templates.md)
* [Automatic persistence of task output files to Azure Storage](../../outputFiles.md)
* [Easy software installation via package managers](../../packages.md)
* [Parametric sweep task factory](../../taskFactories.md#parametric-sweep)
* [Task per file task factory](../../taskFactories.md#task-per-file)

## Prerequisites

You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

## Create a pool

Create your pool using the default settings:
``` bash
azure batch pool create --template pool.json
```

The default settings create pool a named `ffmpeg-pool` with **3** x **STANDARD_D1 VM** virtual machines. 

If you want to change the default values of the pool creation,  create a JSON file to supply the parameters of your pool. If you have a large number of media files to convert, you should use a larger pool or bigger VMs in the pool. 

In order to create the pool with your own configurations, run instead:
``` bash
azure batch pool create --template pool.json --parameters <your settings JSON file>
```

**You are billed for your Azure Batch pools, so don't forget to delete this pool through the [Azure portal](https://portal.azure.com) when you're done.** 

## Using a parametric sweep for processing

### Upload files

Upload your WAV media files by running this command on a folder containing media files (`*.wav`). 

``` bash
azure batch file upload <path> <group>
```
The parametric sweep expects the files to be named `sample1.wav`, `sample2.wav`, `sample3.wav` and so on - each with the prefix `sample` and an increasing index number. It's important that your files are sequentially numbered with no gaps.

### Configure parametric sweep parameters

Modify `job.parameters.json` to supply parameters to the template. If you want to configure other options of the job, such as the the pool id, look in the `job.sweep.json` parameters section to see what options are available.

| Parameter            | Required  | Description                                                                                                                                                                   |                                                                                                                                                                        |
| -------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| poolId               | Optional  | Name of the Azure Batch Pool to use for processing. <br/> Must match the pool you created earlier. Default value if not otherwise specified: `ffmpeg-pool`.                    |                                                                                                                                                                        |
| inputFileGroup       | Mandatory | Name of the file group in your storage account containing the files to process. <br/> Must match the name of the group used in the `azure batch file upload` command earlier. |                                                                                                                                                                        |
| outputFileStorageUrl | Mandatory | SAS enabled URL to a writable storage container for the output files.                                                                                                         |                                                                                                                                                                        |
| jobId                | Mandatory | Unique id of the job for processing. <br/> Must not duplicate the `id` of any existing job.                                                                                   |                                                                                                                                                                        |
| taskStart            | Mandatory | The index # of the first file for processing. <br/>Must match the index of the first WAV file you uploaded earlier. <br/>e.g. specify `1` to reference `sample1.wav`.         |                                                                                                                                                                        |
| taskEnd              | Mandatory | The index # of the last file for processing. <br/>Must match the index of the last WAV file you uploaded earlier. <br/> e.g. specify `10` to reference `sample10.wav`.        |                                                                                                                                                                        |

### Run the job with tasks generated by a parametric sweep

To create your job and tasks:

``` bash
azure batch job create --template job.sweep.json --parameters job.parameters.json
```

## Using a task per file for processing

### Upload files

Upload your WAV media files by running this command on a folder containing media files (*.wav):

``` bash
azure batch file upload <path> <group>
```

Unlike the sample using parametric sweep, there's no requirement for your filenames to confirm to a specific pattern.

### Configure task per file parameters

Modify  `job.parameters.json` file to supply parameters to the template. If you want to configure other options of the job, such as the the pool id, you can look in the `job.perFile.json` parameters section to see what options are available.

| Parameter            | Required  | Description                                                                                                                                                                   |
| -------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| poolId               | Optional  | Name of the Azure Batch Pool to use for processing. <br/> Must match the pool you created earlier. Default value if not otherwise specified: `ffmpeg-pool`.                    |
| inputFileGroup       | Mandatory | Name of the file group in your storage account containing the files to process. <br/> Must match the name of the group used in the `azure batch file upload` command earlier. |
| outputFileStorageUrl | Mandatory | SAS enabled URL to a writable storage container for the output files.                                                                                                         |
| jobId                | Mandatory | Unique id of the job for processing. <br/> Must not duplicate the `id` of any existing job.                                                                                   |

### Run the job with tasks generated per input file

To create your job and tasks:
``` bash
azure batch job create --template job.perFile.json --parameters job.parameters.json
```

## Monitor the job

``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

The outputs of the tasks will be uploaded to the Azure Storage container which you specified as the individual tasks complete.
The target container will contain a new virtual directory for each task that ran.

## Structure of the sample

| File                  | Content                                                                                                                                                                                                                                                                                                                 |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pool.json`           | A template for creating a pool for processing with `ffmpeg`. <br/> By default, this template will create a pool called `ffmpeg-pool` containing **3** x **STANDARD_D1** virtual machines.<br/> You will need to create a parameter file (with suggested name `pool.parameters.json`) if you want to customize the pool. |
| `job.sweep.json`      | A template for creating a job that uses a parametric sweep to process a set of sequentially numbered input files with `ffmpeg`.                                                                                                                                                                                         |
| `job.parameters.json` | Specifies values for the parametric sweep parameters defined in the file `job.sweep.json`. You will need to provide values for the placeholders present in this file before creating your job.                                                                                                                          |
| `job.perFile.json`    | A template for creating a job that uses a per-file task factory to process a set of input files with `ffmpeg`.                                                                                                                                                                                                          |
