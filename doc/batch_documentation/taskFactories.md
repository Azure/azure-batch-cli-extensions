# Task factories

Task factories provide a way for a job and all its tasks to be created in one command instead
of calling `azure batch task create` for each task.

**Note:** If the CLI should lose connectivity during the addition of tasks, the operation will not be completed and the job
will continue with a partial set of tasks. The remainder of the tasks must be added manually using `azure batch task create`.

There are currently three kinds of task factories:

* Task Collection - tasks are explicitly defined as a part of the job
* Parametric Sweep - a set of tasks are created by substituting a range or sequence of values into a template 
* Per File - a template task is replicated for each available input file 

See below for details.

## Task collection 

This task factory is where each task is individually specified according to the 
[Batch API schema](https://msdn.microsoft.com/library/azure/dn820105.aspx).
The `task collection` task factory most closely mirrors the Batch task creation API.

An example of a `task collection` task factory:
```json
  "job": {
    "id": "my-ffmpeg-job",
    "constraints": {
      "maxWallClockTime": "PT5H",
      "maxTaskRetryCount": 3
    },
    "poolInfo": {
      "poolId": "my-ffmpeg-pool"
    },
    "jobPreparationTask": {
      "commandLine" : "sudo apt-get install ffmpeg -y",
      "runElevated": true,
      "waitForSuccess": true
    },
    "taskFactory": {
      "type": "taskCollection",
      "tasks": [
        {
          "id" : "mytask1",
          "commandLine": "ffmpeg -i sampleVideo1.mkv -vcodec copy -acodec copy output.mp4 -y",
        },
        {
          "id" : "mytask2",
          "commandLine": "ffmpeg -i sampleVideo2.mkv -vcodec copy -acodec copy output.mp4 -y",
        }
      ]
    }
  }
```


### Samples

The following samples use the task collection task factory:

* [MPI](samples/mpi)

## Parametric sweep

The `parametric sweep` task factory creates a set of tasks by substituting a range or sequence
of values into a template. Substitutions can be made in most attributes of the task, but are most commonly
made in the commandLine attribute or resourceFile collection.

Currently the following task attributes are not supported in a parametric sweep task factory:
- `id`: The ID of a task will be automatically generated.
- `dependsOn`: Dependencies between tasks within a factory, or tasks created by other means are not yet supported. 

An example:
```json
  "job": {
    "id": "my-ffmpeg-job",
    "poolInfo": {
      "poolId": "my-ffmpeg-pool"
    },
    "taskFactory": {
      "type": "parametricSweep",
      "parameterSets": [
          {
              "start": 1,
              "end": 500,
              "step": 1
          }
      ],
      "repeatTask": {
          "commandLine": "ffmpeg -i sampleVideo{0}.mkv -vcodec copy -acodec copy output{0}.mp4 -y",
      }
    }
  }
```

The range of values used to create the tasks are set in `parameterSets`. The first task to be created is represented
by the `start` field, and the last that that could potentially be created is represented by the `end` field. Whether
this last task is created will depend on the chosen increment size; the vlaue of `step`.
For example, a parameteric sweep with a `start` of 5, `end` of 10 and a `step` of 3 will produce two tasks using the values 5 and 8.

Multiple `parameterSets` can be defined to produce multi-dimensional parametric sweeps.

The task template into which the parameter or parameters will be substituted is defined in `repeatTask`. Substitutions are achieved
through the use of placeholders. A placeholder for parameter substitutions is represented by `{0}`. The number 0 here represents
the index of the parameter set to be substituted. Where a literal `{` or `}` character is required, it can be escaped 
by duplicating it: `{{` or `}}`. The parameter can also be padded with zeros to a maximum length of 9 characters by using the format
`{0:4}` where the number 0 represents the index of the parameter set and the parameter will be zero-padded to 4 characters, e.g.: `0001`. 

The above task factory would be expanded into the following tasks:
```
  "tasks": [
    {
      "id" : "0",
      "commandLine": "ffmpeg -i sampleVideo1.mkv -vcodec copy -acodec copy output1.mp4 -y",
    },
    {
      "id" : "1",
      "commandLine": "ffmpeg -i sampleVideo2.mkv -vcodec copy -acodec copy output2.mp4 -y",
    },
    {
      ...
    },
    {
      "id" : "499",
      "commandLine": "ffmpeg -i sampleVideo500.mkv -vcodec copy -acodec copy output500.mp4 -y",
    }
  ]
```

An example of a task factory with a two-dimensional sweep with zero-padding:

```json
  "job": {
    "id": "my-ffmpeg-job",
    "poolInfo": {
      "poolId": "my-ffmpeg-pool"
    },
    "taskFactory": {
      "type": "parametricSweep",
      "parameterSets": [
        {
          "start": 1,
          "end": 500,
          "step": 1
        },
        {
          "start": 500,
          "end": 1000,
          "step": 500
        }
      ],
      "repeatTask": {
        "commandLine": "ffmpeg -i sampleVideo_{0:3}.mkv -vcodec copy -acodec copy scale={1}:{1} output_x{1}_{0:3}.mp4 -y",
      }
    }
  }
```

Where the following tasks would be created:
```
  "tasks": [
    {
      "id" : "0",
      "commandLine": "ffmpeg -i sampleVideo_001.mkv -vcodec copy -acodec copy scale=500:500 output_x500_001.mp4 -y",
    },
    {
      "id" : "1",
      "commandLine": "ffmpeg -i sampleVideo_001.mkv -vcodec copy -acodec copy scale=1000:1000 output_x1000_001_.mp4 -y",
    },
    {
      "id" : "2",
      "commandLine": "ffmpeg -i sampleVideo_002.mkv -vcodec copy -acodec copy scale=500:500 output_x500_002.mp4 -y",
    },
    {
      "id" : "3",
      "commandLine": "ffmpeg -i sampleVideo_002.mkv -vcodec copy -acodec copy scale=1000:1000 output_x1000_002.mp4 -y",
    },
    {
      ...
    },
    {
      "id" : "998",
      "commandLine": "ffmpeg -i sampleVideo500.mkv -vcodec copy -acodec copy scale=500:500 output_x500_500.mp4 -y",
    },
    {
      "id" : "999",
      "commandLine": "ffmpeg -i sampleVideo500.mkv -vcodec copy -acodec copy scale=1000:1000 output_x1000_500.mp4 -y",
    }
  ]
```

### Samples

The following samples use the parametric sweep task factory:

* [Blender](samples/blender) 
* [Blender with application templates](samples/blender-appTemplate)
* [Create Pool and Job with templates](samples/hello-world/create-pool-and-job-with-templates)
* [FFMpeg](samples/ffmpeg)
* [OCR](samples/ocr)


## Task per file

The `task per file` task factory generates a task per input file from a file group or Azure storage container. Substitutions can be made in most attributes of the task, but are most commonly
made in the commandLine attribute, resourceFile collection or taskOutput attribute.

Currently the following task attributes are not supported in a task per file task factory:
- `id`: The ID of a task will be automatically generated.
- `dependsOn`: Dependencies between tasks within a factory, or tasks created by other means are not yet supported. 

An example:
```json
  "job": {
    "id": "my-ffmpeg-job",
    "poolInfo": {
      "poolId": "my-ffmpeg-pool"
    },
    "taskFactory": {
      "type": "taskPerFile",
      "source": {
        "fileGroup": "raw-images"
      },    
      "repeatTask": {
        "commandLine": "ffmpeg -i {fileName} -vcodec copy -acodec copy {fileNameWithoutExtension}.mp4 -y",
        "resourceFiles": [
          {
            "blobSource": "{url}",
            "filePath" : "{fileName}" 
          }
        ]
      }
    }
  }
```

The list of files used to create the tasks are set in `source`. Similar to new `ResourceFiles` property, there are two ways to specify the file container in Azure Storage. 
1. Specify the name of a file group to reference data stored in a linked storage account.
2. Specify the full container URL include the SAS key which has to have List and Read permission. For example:
```json
  "source": {
	  "containerUrl": "https://storage.blob.core.windows.net/container?sv=2015-04-05sig=tAp0r3I3SV5PbjpZ5CIjvuo1jdUs5xW"
  }    
```
The files can be further filtered by including a prefix. This prefix can be a partial filename, or a subdirectory. If prefix is not specified, all the files in the container will be used for creating task. An example using prefix:
```json
  "source": {
	  "fileGroup": "raw-images",
	  "prefix": "first_pass/img_"
  }    
```

The task template into which the file URL/name will be substituted is defined in `repeatTask`. Substitutions are achieved
through the use of placeholders. A placeholder for name substitutions is represented by `{keyword}`. The keyword here represents
which part of file URL to be substituted. The supported keyword are:

| Keyword                      | Note                                                 | Example                                                        |
| ---------------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| `{url}`                      | The full URL of file location                        | http://account.blob.azure.com/container/path/blob.ext?sasToken |
| `{filePath}`                 | The file name including the path (virtual directory) | path/blob.ext                                                  |
| `{fileName}`                 | The file name only, without path                     | blob.ext                                                       |
| `{fileNameWithoutExtension}` | The file name without last extension                 | blob                                                           |

Where a literal `{` or `}` character is required, it can be escaped by duplicating it: `{{` or `}}`.

For example, if the files in file group are:
```
raw-images/first_pass/mov_processing/1.mkv
raw-images/first_pass/mov_processing/2.mkv
raw-images/first_pass/alpha.mkv
```
The above task factory would be expanded into the following tasks:

```json
  "tasks": [
    {
      "id" : "0",
      "commandLine": "ffmpeg -i 1.mkv -vcodec copy -acodec copy 1.mp4 -y",
      "resourceFiles": [
        {
          "blobSource": "http://account.blob.azure.com/raw-images/first_pass/mov_processing/1.mkv?sasToken",
          "filePath" : "1.mkv" 
        }
      ]
    },
    {
      "id" : "1",
      "commandLine": "ffmpeg -i 2.mkv -vcodec copy -acodec copy 2.mp4 -y",
      "resourceFiles": [
        {
          "blobSource": "http://account.blob.azure.com/raw-images/first_pass/mov_processing/2.mkv?sasToken",
          "filePath" : "2.mkv" 
        }
      ]
    },
    {
      "id" : "2",
      "commandLine": "ffmpeg -i alpha.mkv -vcodec copy -acodec copy alpha.mp4 -y",
      "resourceFiles": [
        {
          "blobSource": "http://account.blob.azure.com/raw-images/first_pass/alpha.mkv?sasToken",
          "filePath" : "alpha.mkv" 
        }
      ]
    }
  ]
```

### Samples

The following samples use the task per file task factory:

* [Task Per File](samples/hello-world/task-per-file)
* [Create Pool and Job with templates](samples/hello-world/create-pool-and-job-with-templates)
* [Task Per File](samples/hello-world/task-per-file)
* [FFMpeg](samples/ffmpeg)

