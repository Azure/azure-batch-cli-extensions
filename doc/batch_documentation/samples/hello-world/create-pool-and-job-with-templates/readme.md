# Azure Batch Pool/Job Template

This sample shows how to create a pool, and run a parametric sweep job on it, using *parameterized* templates for both the pool and the job.

## Features used by this sample

* [Pool and job templates with parameterization](../../templates.md)
* [Parametric sweep task factory](../../taskFactories.md#parametric-sweep)
* [Task per file task factory](../../taskFactories.md#task-per-file)

## Prerequisites

You will need an Azure Batch account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

## Preparation

Modify the parameters specified in `pool.parameters.json` to configure your pool. Available parameters are defined in `pool.json`:

| Parameter | Required  | Description                                                                                                                 |
| --------- | --------- | --------------------------------------------------------------------------------------------------------------------------- |
| poolId    | Mandatory | Unique id of the Azure Batch pool to create.                                                                            |
| vmCount   | Optional  | Number of virtual machines. <br/> Defaults to **3** if not otherwise specified.                                         |
| vmSize    | Optional  | Size of the virtual machines that run the application. <br/> Defaults to **STANDARD_D1_V2** if not otherwise specified. |

Modify the parameters specified `job.parameters.json` as appropriate to configure your job. Available parameters are defined in `job.json`:

| Parameter | Required  | Description                                                                                                    |
| --------- | --------- | -------------------------------------------------------------------------------------------------------------- |
| jobId     | Mandatory | Unique id of the Azure Batch job to create.                                                                    |
| poolId    | Mandatory | Unique id of Azure Batch pool which runs the job. <br/> Must match the `poolId` used for the pool (see above). |
| taskStart | Mandatory | Start index of the parametric sweep.                                                                           |
| taskEnd   | Mandatory | Finishing index (inclusive) of the parametric sweep.                                                           |

## Run commands

To create your pool:
``` bash
azure batch pool create --template pool.json --parameters pool.parameters.json
```

**You are billed for your Azure Batch pools, so don't forget to delete this pool through the [Azure portal](https://portal.azure.com) when you're done.** 

To create your job:
``` bash
azure batch job create --template job.json --parameters job.parameters.json
``` 

## Monitor the job
You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample

| File                   | Content                                                                                                                                                                                                                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `pool.json`            | A template for defining a new pool.                                                                                                                                                                                                                                                              |
| `pool.parameters.json` | Provides values for the parameters defined in `pool.json`. <br/> You will need to provide a value for `poolId` before pool creation will succeed. If you do not want to use the default values for `vmCount` or `vmSize`, add values for those parameters to this file before creating the pool. |
| `job.json`             | A template for a new job.                                                                                                                                                                                                                                                                        |
| `job.parameters.json`  | Provides values for the parameters defined in `job.json`. <br/> You will need to provide actual values for these parameters before job creation will succeed.                                                                                                                                    |

Note that the **taskFactory** feature used in `job.json` is an experimental feature currently only available through the XPlat CLI.

## Troubleshooting

### "The value provided for one of the properties in the request body is invalid."

This error will occur during pool creation if you have not modified the `pool.parameters.json` to provide a legal pool id.

This error will occur during job creation if you have not modified the parameters in `job.parameters.json` to specify the job id, pool id and so on.

In either case, review the `azure.err` listed in the logs to see more details about the error.

