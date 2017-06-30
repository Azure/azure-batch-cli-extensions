# Output files to a file group

When specifying output files for your tasks, you can now specify a file group to upload
the outputs.

```json
{
  "id" : "2",
  "commandLine": "ffmpeg -i sampleVideo2.mkv -vcodec copy -acodec copy outputVideo2.mp4 -y",
  "outputFiles": [
      {
        "filePattern": "outputVideo2.mp4",
        "destination": {
          "autoStorage": {
            "path": "mytask2output.mp4",
            "fileGroup": "output-videos"
          }
        },
        "uploadOptions": {
          "uploadCondition": "TaskSuccess"
        }
      },
      {
        "filePattern": "../stderr.txt",
        "destination": {
          "autoStorage": {
            "path": "ffmpeg/2_error.log",
            "fileGroup": "job-logs"
          }
        },
        "uploadOptions": {
          "uploadCondition": "TaskFailure"
        }
      }
    ]
}
```

## Options

| Property      | Required  | Type         | Description                                                                                                                                                                                             |
| ------------- | --------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filePattern   | Mandatory | String       | The name of the file or files to be uploaded. This could be an absolute path, or a path relative to the task working directory. This can be a single file, or a pattern using wildcards (`**` and `*`). |
| destination   | Mandatory | Complex Type | The destination to which the output files specified in `filePattern` will be uploaded.                                                                                                                  |
| uploadOptions | Mandatory | Complex Type | The details regarding the upload conditions.                                                                                                                                                            |

### destination

| Property    | Required | Type         | Description                                                                                                                |
| ----------- | -------- | ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| container   | Optional | Complex Type | Details of the destination container. The `container` property is mutually exclusive with `autoStorage` property, one of which must be supplied.          |
| autoStorage | Optional | Complex Type | Details of the destination under auto-storage. The `autoStorage` property is mutually exclusive with `container` property, one of which must be supplied. |

### container

| Property     | Required  | Type   | Description                                                                                                                                                                                                                                        |
| ------------ | --------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| path         | Optional  | String | Path within the container to which data will be uploaded. If `filePath` refers to multiple files, `path` will be considered a virtual directory within the container. Otherwise `path` will be considered to include the filename used in storage. |
| containerSas | Optional  | String | The SAS URL to the storage container used to hold the output data. The SAS must have write permissions. <br/> Note: A SAS URL to your entire storage account will not work, nor will one that has expired.                                         |

### autoStorage

| Property     | Required  | Type   | Description                                                                                                                                                                                                                                           |
| ------------ | --------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| path         | Optional  | String | Path within the file group to which data will be uploaded. If `filePath` refers to multiple files, `path` will be considered a virtual directory within the file group. Otherwise `path` will be considered to include the filename used in storage. |
| fileGroup    | Optional  | String | The file group stored in linked storage.                                                                                                                                                                                                              |

### uploadOptions 

| Property   | Required  | Type    | Description                                                  |
| ---------- | --------- | ------- | ------------------------------------------------------------ |
| uploadCondition | Mandatory | String  | Specify circumstances when output files should be persisted. |            

Available options for `uploadCondition` are:

* `TaskSuccess` - Upload if the task completed with an exit code of zero.
* `TaskFailure` - Upload if the task completed with a nonzero exit code.
* `TaskComplete` - Uploaded always (irrespective of the exit code of the task).

## Output File Download

Output files that have been persisted to auto-storage using a file group can be downloaded using an additional CLI command:

```bash
az batch file download --local-path C:\job_outputs\logs --file-group job-logs

az batch file download --local-path /home/job_outputs/logs --file-group job-logs
```

If output files were persisted into a subfolder in the file group, this can be specified using the
`--remote-path` flag. If a file of the same name already exists locally, it will not be overwritten by
default. To overwrite any existing files, use the `--overwrite` flag.

```bash
az batch file download --local-path C:\job_outputs\logs --file-group job-logs --remote-path ffmpeg --overwrite

az batch file download --local-path /home/job_outputs/logs --file-group job-logs --remote-path ffmpeg --overwrite
```

## Samples

The following samples automatically upload their output files as they complete:

* [Task Per File](../samples/hello-world/task-per-file)
* [Blender](../samples/blender) 
* [Blender with application templates](../samples/blender-appTemplate)
* [FFMpeg](../samples/ffmpeg)
* [OCR](../samples/ocr)

## Troubleshooting

### Files do not upload to blob storage

If there are no files uploaded to blob storage when your task completes, check error messages in an `uploadlog.txt` file on the node that ran the task. (You can do this from the [Azure portal](https://portal.azure.com)).
