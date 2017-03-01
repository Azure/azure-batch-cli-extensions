# Input files

## Input file upload

We have introduced a new command to allow a user to upload job input data directly
to the storage account linked to their Azure Batch.
The uploaded files will be stored under a name, or `file group` that can be referenced by any job run
within that Batch Account. For examples on how to use the data in a file group, see [Referencing input data](#referencing-input-data)

The data will also be stored in a way so as to preserve the local directory structure, allowing 
this to be recreated on the compute node.

Example local input data:
```
data/img_processing/1.png
data/img_processing/2.png
data/img_processing/3.png
data/alpha.png
data/rgb.png
data/1.png
```

Example command:
```bash
azure batch file upload C:\data\**\*.png raw-images

azure batch file upload /tmp/data/**/*.png raw-images
```

In the above commands, all the PNG files in the `data` directory (C:\\data or /tmp/data) will be uploaded to a linked storage account under
a file group named "raw-images". Any subdirectory structure relative to the `data` directory will 
be retained.
If any of the data already exists in the file group, only data that has since been modified will be uploaded to overwrite existing files.

Resulting structure:
```
raw-images/img_processing/1.png
raw-images/img_processing/2.png
raw-images/img_processing/3.png
raw-images/alpha.png
raw-images/rgb.png
raw-images/1.png
```

### Other options

#### flatten

This will discard the local directory structure and upload files to a flattened structure.
Example command:
```bash
azure batch file upload C:\data\**\*.png raw-images --flatten

azure batch file upload /tmp/data/**/*.png raw-images --flatten
```

Resulting structure:
```
raw-images/1.png
raw-images/2.png
raw-images/3.png
raw-images/alpha.png
raw-images/rgb.png
```
Notice that in the above example we have a name collision. When `flatten` is used, multiple files of the same name that were 
previously distinguished by a unique file path will not be supported regardless of the content of the file. 
Files of the same name will be compared by their date of last modification, and only the most recently modified will be stored.


#### path

This will upload any data into a subdirectory within the file group. This directory will also
be created on the compute node. Example command:
```bash
azure batch file upload C:\data\**\*.png raw-images --path first_pass

azure batch file upload /tmp/data/**/*.png raw-images --path first_pass
```

Resulting structure:
```
raw-images/first_pass/img_processing/1.png
raw-images/first_pass/img_processing/2.png
raw-images/first_pass/img_processing/3.png
raw-images/first_pass/alpha.png
raw-images/first_pass/rgb.png
raw-images/first_pass/1.png
```

You can also combine `path` and `flatten` like so:
```bash
azure batch file upload C:\data\**\*.png raw-images --path first_pass --flatten

azure batch file upload /tmp/data/**/*.png raw-images --path first_pass -flatten
```

Resulting structure:
```
raw-images/first_pass/1.png
raw-images/first_pass/2.png
raw-images/first_pass/3.png
raw-images/first_pass/alpha.png
raw-images/first_pass/rgb.png
```


## Referencing input data

Input data stored in linked storage under a file group can be simply referenced by a task 
(including Job Preparation and Release tasks, Job Manager tasks and Pool Start tasks)
by using some new ResourceFile properties.

Example input data in in the file group `raw-images`:
```
raw-images/first_pass/img_processing/1.png
raw-images/first_pass/img_processing/2.png
raw-images/first_pass/img_processing/3.png
raw-images/first_pass/alpha.png
raw-images/first_pass/rgb.png
raw-images/first_pass/1.png
image-config-data/first_pass/img_config_2016.cfg
image-config-data/second_pass/img_config_2016.cfg
```

Example JSON:
```json
"resourceFiles": [
  {
    "source": { 
      "fileGroup": "raw-images",
    }
  },
  {
    "source": { 
      "fileGroup": "image-config-data",
    }
  }
]
```
The above schema will include all the data found in the specified file groups with the job.

Files on node (where `wd` refers to the task current working directory):
```
wd/first_pass/img_processing/1.png
wd/first_pass/img_processing/2.png
wd/first_pass/img_processing/3.png
wd/first_pass/alpha.png
wd/first_pass/rgb.png
wd/first_pass/1.png
wd/first_pass/img_config_2016.cfg
wd/second_pass/img_config_2016.cfg
```

The data can be further filtered by including a prefix. This prefix can be a
whole filename, partial filename, or a subdirectory.

 ```json
"resourceFiles": [
  {
    "source": { 
      "fileGroup": "raw-images",
      "prefix": "first_pass/img_"
    }
  },
  {
    "source": { 
      "fileGroup": "image-config-data",
      "prefix": "first_pass/img_config_2016.cfg"
    }
  }
]
```
Files on node:
```
wd/first_pass/img_processing/1.png
wd/first_pass/img_processing/2.png
wd/first_pass/img_processing/3.png
wd/first_pass/img_config_2016.cfg
```

Finally, you can also specify the path to which the files will be downloaded on the 
compute node. If the source reference is a single file, the specified `filePath` is assumed
to include the filename. Otherwise, if the source references multiple files, 
`filePath` will be treated as a directory.
In the case where `filePath` is used as a directory, any directory structure already associated
with the input data will be retained in full and appended to the specified `filePath` directory and recreated
within the specified directory.

```json
"resourceFiles": [
  {
    "source": { 
      "fileGroup": "raw-images",
      "prefix": "first_pass/img_"
    },
    "filePath": "images"
  },
  {
    "source": { 
      "fileGroup": "image-config-data",
      "prefix": "first_pass/img_config_2016.cfg"
    },
    "filePath": "images/first_pass.cfg"
  }
]
```
Files on node:
```
wd/images/first_pass/img_processing/1.png
wd/images/first_pass/img_processing/2.png
wd/images/first_pass/img_processing/3.png
wd/images/first_pass.cfg
```

## Samples

The following samples automatically use the upload feature to make files available for processing

* [Blender](samples/blender) 
* [Task Per File](samples/hello-world/task-per-file)
* [OCR](samples/ocr)


