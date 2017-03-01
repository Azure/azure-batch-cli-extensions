# Job and pool templates with parameterization

Two new options have been introduced to the `batch job create` and `batch pool create` commands:
- `--template`
  - The path to a JSON file with the template for either a Batch job or pool.
- `--parameters`
  - The path to a JSON file containing parameter values. When used exclusive of `--template` this option will be ignored.

```bash
azure batch job create --template <JSON template> --parameters <JSON parameter values>
```

The format of this template draws on the structure of an Azure Resource Manager template.
The structure of template consists of the following sections:
- `parameters`: (Optional) Values that are provided during execution to customize the entity.
- `variables`: (Optional) Values that are used as JSON fragments in the template.
- `job` or `pool`: (Required) The entity description to be created.

For further reading on ARM templates, see [Authoring Azure Resource Manager templates](https://azure.microsoft.com/documentation/articles/resource-group-authoring-templates).

## Samples

The following samples make use of job and/or pool templates:

* [Create Pool and Job with templates](samples/hello-world/create-pool-and-job-with-templates)
* [Task Per File](samples/hello-world/task-per-file)
* [Blender](samples/blender) 
* [FFMpeg](samples/ffmpeg)
* [MPI](samples/mpi)
* [OCR](samples/ocr)

## Parameters

This section consists of a set of parameter definitions, with accompanying metadata and constraints.
For example: 
```json
{
    "parameters": {
        "poolId": {
            "type": "string",
            "metadata": {
                "description": "The ID of Azure Batch pool which runs the job"
            }
        }
    }
}
```
Parameters can be referenced using ARM-template parameter syntax: `[parameters('parameterName')]`.

The following options for a parameter are currently supported:
- `type`
    - `int`, `string` or `bool`
- `defaultValue`
- `allowedValues`
- `minValue`
- `maxValue`
- `minLength`
- `maxLength`
- `metadata`
    - `description`

## Variables

In this section you can construct complex JSON fragments that can be used throughout the template. Typically
variables also include references to values defined in `parameters`. Variables can be referenced using ARM-template variable syntax: `[variables('variableName')]`. 

For example:
```json
{
    "variables": {
        "pool": {
            "poolInfo": {
                "poolId": "[parameters('poolId')]"
            }
        }
    }
}
```

## Defining the job or pool entity

The job or pool to be created adheres to the same schema as the request body found in the 
[Batch API documentation](https://msdn.microsoft.com/library/azure/dn820110.aspx) and is wrapped in a `properties` layer consistent
with the structure of an [ARM resource](https://azure.microsoft.com/documentation/articles/resource-group-authoring-templates/#resources).
A `type` field is also present, referencing the entity type to be created. Other ARM options (for example `location` or `dependsOn`) will be ignored.
Valid `type` options are:
- `"Microsoft.Batch/batchAccounts/jobs"`
- `"Microsoft.Batch/batchAccounts/pools"`

**Note:** Unlike true ARM templates, Batch CLI templates must contain only a single definition for either a Batch job or pool.
Additionally, not all ARM template syntax is supported. We currently support the following expressions and functions:

- `parameters()`: A function to inject the value of a defined parameter into the JSON.
    - Example: `"id": "[parameters('jobId')]"`
- `variables()`: A function to inject the fragment of a defined variable into the JSON.
    - Example: `"poolInfo": "[variables('autoPool')]"`
- `concat()`: A function to join two strings together.
    - Example: `"displayName": "[concat("Processing: ", parameters('inputName'))]"`

Example templates and their accompanying parameter files can be found at
[Documentation/BatchDocumentation/samples](Documentation/BatchDocumentation/samples).

A simple parameterized template might look like this:
```json
{
    "parameters": {
        "poolId": {
            "type": "string",
            "defaultValue": "testpool",
            "metadata": {
                "description": "The ID of the Batch pool on which to run the job"
            }
        },
        "jobId": {
            "type": "string",
            "metadata": {
                "description": "The ID of the Batch job"
            }
        }
    },
    "job": {
        "type": "Microsoft.Batch/batchAccounts/jobs",
        "properties": {
            "id": "[parameters('jobId')]",
            "poolInfo": {
                "poolId": "[parameters('poolId')]"
            }
        }
    }
}
```

You could then run this template with the following command:

```bash
azure batch job create --template my-simple-job.json
```

The values of the parameters will either use a default value if supplied,
or the CLI will interactively prompt you to provide an input value.
Alternatively, you can supply these parameter values in a separate file, like so:

```json
{
  "jobId": {
    "value": "test_job"
  },
  "poolId": {
    "value": "ubuntu_16_04"
  }
}
```

You can then pass this parameter file to the job create command:

```bash
azure batch job create --template my-simple-job.json --parameters my-input-values.json
```
