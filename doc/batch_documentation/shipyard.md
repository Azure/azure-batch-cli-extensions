# Batch Shipyard integration and Docker Support

The Azure Batch preview CLI integrates with Batch Shipyard to allow you to provision Batch compute nodes with Docker containers and to schedule Docker workloads. For more information on Batch Shipyard, see its [GitHub page](https://github.com/azure/batch-shipyard).

**Note:** This feature is only available on Linux VMs.

In order to use Docker containers with the Azure Batch preview CLI, the following prerequisites must also be installed locally:
- You must install Python (2.7 or 3.3+), and it must be available on the PATH.
- You must install Batch Shipyard. See the [installation guide](https://github.com/Azure/batch-shipyard/blob/2.2.0/docs/01-batch-shipyard-installation.md) for more details. The Azure Batch CLI currently targets Batch Shipyard version 2.2.0. Compatibility with other versions is not guaranteed.

## Provisioning a pool to use Docker containers:

To provision Batch compute nodes that use Docker containers, you must supply a `clientExtensions.dockerOptions` definition in the JSON request you pass to the `batch pool create` command (either with `--json-file` or `--template`. The following is the dockerOptions schema:
`dockerOptions`: 
* `image`: (required, string) The Docker image to install on every compute node when the pool is created.
* `registry`: (optional, object) Configure Docker image distribution options from public/private Docker Hub.
  * `hub`: (optional, object) Docker Hub login settings. This does not need to be supplied if pulling from public Docker repositories.
    * `username`: (required, string) The username to log in with.
    * `password`: (required, string) The password to log in with.
  * `private`: (optional, object) Controls settings for private registries.
    * `allowPublicPullOnMissing`: (required, bool) Whether to allow pass-through of Docker image retrieval to public Docker Hub if the image is missing in the private registry.
* `sharedDataVolumes`: (optional, array) Configures the initialization of persistent shared storage volumes. Each array item has the following properties:
  * `name`: (required, string) The name used to identify the shared data volume. This name is created by the user and only used as a reference in dockerOptions definitions on pool and task bodies.
  * `volumeType`: (required, string) The type of the shared data volume. Currently, the only supported value is "azurefile".
  * `azureFileShareName`: (required, string) The Azure File share name. Note that this share must already be created in the Batch account's linked storage account. The linked storage account must also be in the same region as the Batch account. For more information on linked storage accounts, see [this article](https://azure.microsoft.com/documentation/articles/batch-account-create-portal/#linked-azure-storage-account). 

The following is an example pool specification with its clientExtensions.dockerOptions set.
```json
{
  "pool": {
    "id": "myPool",
    "virtualMachineConfiguration": {
      "imageReference": {
        "publisher": "Canonical",
        "offer": "UbuntuServer",
        "sku": "16.04.0-LTS"
      }
    },
    "vmSize": "STANDARD_D1_V2",
    "targetDedicated": 1,
    "maxTasksPerNode": 1,
    "clientExtensions": {
      "dockerOptions": {
        "image": "batch/images:abc",
        "sharedDataVolumes": [
          {
            "name": "myShare",
            "volumeType": "azurefile",
            "azureFileShareName": "batchclishare"
          }
        ]
      }
    }
  }
}
```

## Scheduling a Docker workflow
To schedule Docker workflows, you must supply a clientExtensions.dockerOptions definition on your task bodies within your taskFactory when using the 'batch job create' command. The following is the dockerOptions schema:
`dockerOptions`:
* `image`: (required, string) The Docker image to use for this task. This image must be available on the pool that the task is scheduled against.
* `additionalDockerRunOptions`: (optional, array) The additional `docker run` option strings to pass to the Docker daemon when starting the container.
* `dataVolumes`: (optional, array) The data volumes to mount in the container. Each array item has the following properties:
  * `hostPath`: (optional, string) The path on the host node which will be mounted in the container. 
  * `containerPath`: (required, string) The path in the container where the data volume will be mounted/found.
* `sharedDataVolumes`: (optional, array) The persisted shared storage volumes to use in the container. Each array item has the following properties:
  * `name`: (required, string) The name used to identify the shared data volume. A volume with this name must have been configured on the pool that the task is scheduled against (i.e. If you reference a shared data volume with name 'myShare' on your task, then you must have a shared data volume with name 'myShare' defined on your pool).
  * `volumeType`: (required, string) The type of the shared data volume. Currently, the only supported value is "azurefile".
  * `containerPath`: (required, string) The path in the container where the shared data volume will be mounted.
* `removeContainerAfterExit`: (optional, bool) Whether the container should be automatically removed after the task completes. If unspecified, the default value of false will be used.
* `useHostInfiniband`: (optional, bool) Whether the container requires access to the Infiniband/RDMA devices on the host. Note that this will automatically force the container to use the host network stack. If unspecified, the default value of false will be used.

The following is an example job specification which uses a `taskCollection` task factory where clientExtensions.dockerOptions are specified:
```json
{
  "job": {
    "id": "myJob",
    "poolInfo": {
      "poolId": "myPool"
    },
    "taskFactory": {
      "type": "taskCollection",
      "tasks": [
        {
          "id": "task01",
          "commandLine": "/opt/runWorkflow.sh",
          "clientExtensions": {
            "dockerOptions": {
              "image": "batch/images:abc",
              "removeContainerAfterExit": true,
              "sharedDataVolumes": [
                {
                  "name": "myShare",
                  "volumeType": "azurefile",
                  "containerPath": "/tmp/sharefiles"
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```

The following is an example job specification which uses a `parametricSweep` task factory where clientExtensions.dockerOptions are specified:
```json
{
  "job": {
    "type": "Microsoft.Batch/batchAccounts/jobs",
    "properties": {
      "id": "myJob",
      "poolInfo": {
        "poolId": "myPool"
      },
      "taskFactory": {
        "type": "parametricSweep",
        "parameterSets": [
          {
            "start": "1",
            "end": "100",
            "step": 1
          }
        ],
        "repeatTask": {
          "commandLine": "/opt/workflow{0}.sh",
          "clientExtensions": {
            "dockerOptions": {
              "image": "batch/images:abc",
              "removeContainerAfterExit": true
            }
          }
        }
      }
    }
  }
}
```