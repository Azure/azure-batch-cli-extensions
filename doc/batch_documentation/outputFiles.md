# Output files

When adding a task, you can now declare a list of output files to be automatically uploaded to 
an Azure Storage container of your choice.

An output file description can be added to a task or Job Manager task (or the taskFactory.repeatTask):
```json
{
  "id" : "2",
  "commandLine": "ffmpeg -i sampleVideo2.mkv -vcodec copy -acodec copy outputVideo2.mp4 -y",
  "outputFiles": [
      {
        "filePattern": "outputVideo2.mp4",
        "destination": {
          "container": {
            "path": "mytask2output.mp4",
            "containerSas": "https://storage.blob.core.windows.net/container?sv=2015-04-05sig=tAp0r3I3SV5PbjpZ5CIjvuo1jdUs5xW"
          }
        },
        "uploadDetails": {
          "taskStatus": "TaskSuccess"
        }
      },
      {
        "filePattern": "../stderr.txt",
        "destination": {
          "container": {
            "path": "2_error.log",
            "containerSas": "https://storage.blob.core.windows.net/container?sv=2015-04-05sig=tAp0r3I3SV5PbjpZ5CIjvuo1jdUs5xW"
          }
        },
        "uploadDetails": {
          "taskStatus": "TaskFailure"
        }
      }
    ]
}
```

Multiple output file descriptions can be included to cover different file patterns and different upload circumstances.
In the above example, if the process completes successfully (the process exits with code 0), then the output will be uploaded,
otherwise the error logs are uploaded for debugging.

## Options

| Property      | Required  | Type         | Description                                                                                                                                                                                             |
| ------------- | --------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filePattern   | Mandatory | String       | The name of the file or files to be uploaded. This could be an absolute path, or a path relative to the task working directory. This can be a single file, or a pattern using wildcards (`**` and `*`). |
| destination   | Mandatory | Complex Type | The destination to which the output files specified in `filePattern` will be uploaded.                                                                                                                  |
| uploadDetails | Mandatory | Complex Type | The details regarding the upload conditions.                                                                                                                                                            |

### destination

| Property  | Required  | Type         | Description                          |
| --------- | --------- | ------------ | ------------------------------------ |
| container | Mandatory | Complex Type | Details of the destination container |

### container

| Property     | Required  | Type   | Description                                                                                                                                                                                                                                        |
| ------------ | --------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| path         | Optional  | String | Path within the container to which data will be uploaded. If `filePath` refers to multiple files, `path` will be considered a virtual directory within the container. Otherwise `path` will be considered to include the filename used in storage. |
| containerSas | Mandatory | String | The SAS URL to the storage container used to hold the output data. The SAS must have write permissions. <br/> Note: A SAS URL to your entire storage account will not work, nor will one that has expired.                                         |

### uploadDetails 

| Property   | Required  | Type    | Description                                                  |
| ---------- | --------- | ------- | ------------------------------------------------------------ |
| taskStatus | Mandatory | String  | Specify circumstances when output files should be persisted. |            

Available options for `taskStatus` are:

* `TaskSuccess` - Upload if the task completed with an exit code of zero.
* `TaskFailure` - Upload if the task completed with a nonzero exit code.
* `TaskComplete` - Uploaded always (irrespective of the exit code of the task).

## Samples

The following samples automatically upload their output files as they complete:

* [Task Per File](samples/hello-world/task-per-file)
* [Blender](samples/blender) 
* [Blender with application templates](samples/blender-appTemplate)
* [FFMpeg](samples/ffmpeg)
* [OCR](samples/ocr)

## Troubleshooting

### Files do not upload to blob storage

If there are no files uploaded to blob storage when your task completes, check error messages in an `uploadlog.txt` file on the node that ran the task. (You can do this from the [Azure portal](https://portal.azure.com)).

