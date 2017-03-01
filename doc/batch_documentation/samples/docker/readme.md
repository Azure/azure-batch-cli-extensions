# Caffe on Docker via Batch Shipyard Integration

This sample shows how to run Caffe in a Docker container on a Batch compute node.

## Features used by this sample

* [Batch Shipyard integration and Docker support](../../shipyard.md)

## Prerequisites

* You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.
* You will need to install Batch Shipyard on your local machine. See the help page on [Batch Shipyard integration and Docker support](../../shipyard.md) for details.
* You must agree to the [Caffe license](https://github.com/BVLC/caffe/blob/master/LICENSE) prior to use.

## Create the pool

The `pool.docker.caffe.json` file contains the following parameters. You may optionally create a `parameters.json` file to provide your own values.

| Parameter | Required  | Description                                                                                         |
| --------- | --------- | --------------------------------------------------------------------------------------------------- |
| poolId    | Optional  | Unique id of the Azure Batch pool to create. Defaults to `docker-caffe` if not otherwise specified. |

When you are ready to create the pool, use this command:

```bash
azure batch pool create --template pool.docker.caffe.json [--parameters parameters.json]
```

**You are billed for your Azure Batch pools, so don't forget to delete this pool through the [Azure portal](https://portal.azure.com) when you're done.**

## Create the job

The `job.docker.caffe.json` file contains the following parameters. You may optionally create a `parameters.json` file to provide your own values.

| Parameter | Required  | Description                                                                                                                                                                      |
| --------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| jobId     | Optional  | Unique id of the Azure Batch job to create. Defaults to `docker-caffe-job` if not otherwise specified.                                                                           |
| poolId    | Optional  | Unique id of the Azure Batch pool which runs the job. Must match the `poolId` used when you created the pool (see above). Defaults to `docker-caffe` if not otherwise specified. |

When you are ready to create the job, use this command:

```bash
azure batch job create --template job.docker.caffe.json [--parameters parameters.json]
```

## Monitor the job

You can use this command to monitor the task in the job and its progress:
``` bash
azure batch task show --job-id <jobid> --id 'task01'
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample

| File                     | Content                                                                                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `pool.docker.caffe.json` | A template defining the pool which will run the job. The pool contains a single compute node which is configured for running Docker containers. |
| `job.docker.caffe.json`  | A template defining the job and a task.   The task will run Caffe in a Docker container.                                                        |