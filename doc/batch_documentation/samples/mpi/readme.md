# Azure Batch MPI Template

This samples shows how to use `MS-MPI` to run MPI work.

## Features used by this sample

* [Pool and job templates with parameterization](../../templates.md)
* [Task collection factory](../../taskFactories.md#task-collection)

## Prerequisites

You must have an Azure Batch account set up with a linked Azure Storage account.

You will need an MS-MPI program for the multi-instance task to execute. We provide the [MPIHelloWorld sample project](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/ArticleProjects/MultiInstanceTasks/MPIHelloWorld) for you to compile and to use as your MS-MPI program. Build a release version of `MPIHelloWorld.exe` so that you don't have to include any additional dependencies (for example, `msvcp140d.dll` or `vcruntime140d.dll`).

## Create application package

To successfully run this sample, you must first create an [application package](https://docs.microsoft.com/azure/batch/batch-application-packages) containing [MSMpiSetup.exe](https://msdn.microsoft.com/library/bb524831.aspx) (installed on a pool's compute nodes with a start task).

The following commands can be used as example to create the application package:

First, create the application package `MSMPI` itself:

```bash
azure batch application create --application-id MSMPI --account-name <account name> --resource-group <resource group>
```
You will need to supply your own values for `<account name>` and `<resource group>`.

Create a zip file containing `MSMpiSetup.exe` (make sure this file is at the root of zip file). Create version `1.0` of the application `MSMPI`:

```bash
azure batch application package create --application-id MSMPI --version 1.0 --account-name <account name> --resource-group <resource group> --package-file <local path to MSMpiSetup.exe zip file>
```

Then, activate the application package `MSMPI:1.0`:

```bash
azure batch application package activate --application-id MSMPI --version 1.0 --account-name <account name> --resource-group <resource group> --format zip
```

Finally, set the application default version to `1.0`:

```bash
azure batch application set --application-id MSMPI --default-version 1.0 --account-name <account name> --resource-group <resource group>
```

## Create a pool

Create your pool:

```bash
azure batch pool create --template pool.json
```
The default settings in `pool.json` specify a pool named `MultiInstanceSamplePool` containing **3** **small** virtual machines.

If you want to change the default values of the pool creation, create a JSON file to supply the parameters of your pool and include it on your command line:

```bash
azure batch pool create --template pool.json --parameters <your settings JSON file>
```

**You are billed for your Azure Batch pools, so don't forget to delete this pool through the [Azure portal](https://portal.azure.com) when you're done.** 

## Upload files

Upload the `MPIHelloWorld.exe` application and its dependencies from a folder:

```bash
azure batch file upload <path> mpi
```

`mpi` is the default value of the inputFileGroup parameter in the job template. If you upload your files to a different file group, be sure to provide this value for the inputFileGroup parameter when creating your job (see the next section).

## Create a job with an MPI task

To create your job with default settings:

```bash
azure batch job create --template job.json
```

If you want to configure other options of the job, such as the the pool id, you can look in the `job.json` parameters section to see what options are available.

| Parameter            | Required  | Description                                                                                                                                                                   |
| -------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| poolId               | Optional  | Name of the Azure Batch Pool to use for processing. <br/> Must match the pool you created earlier. Default value if not otherwise specified: `MultiInstanceSamplePool`.       |
| inputFileGroup       | Optional  | Name of the file group in your storage account containing the files to process. <br/> Must match the name of the group used in the `azure batch file upload` command earlier. <br/> Default value if not otherwise specified: `mpi`. |
| vmCount              | Optional  | The number of VM instances to execute the multi-instance task on. <br/> It must be less than or equal to the pool's VM count. Default value if not otherwise specified: 3     |
| jobId                | Mandatory | Unique id of the job for processing. <br/> Must not duplicate the `id` of any existing job.                                                                                   |

To create a job with a different configuration: 

```bash
azure batch job create --template job.json --parameters <your settings JSON file>
```

## Monitor the job

You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.
