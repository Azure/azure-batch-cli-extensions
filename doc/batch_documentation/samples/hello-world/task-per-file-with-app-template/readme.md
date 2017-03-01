# Azure Batch data movement using application templates

This sample shows how to create a job using an *application template* to separate the logic of processing from administration and management. This sample also demonstrates how to use `ResourceFiles` and `OutputFiles` to automatically download files to the virtual machine and to upload the output after the task completes.

With an application template, the processing steps required for the job are defined in a separate file (see the file `movement-template.json`) which is appropriately parameterized. The job itself references the template, supplies any required parameter values and specifies the pool on which the job is to run.

This particular *application template* runs a simple commandline (`cat {fileName}`) for each of the files found in a specified file group from blob storage.

## Features used by this sample

* [Split job configuration and management with reusable application templates](../../../application-templates.md)
* [Task per file task factory](../../../taskFactories.md#task-per-file)
* [Automatic persistence of task output files to Azure Storage](../../../outputFiles.md)

## Prerequisites

You will need an Azure Batch account with a linked Azure Storage account. See [Create an Azure Batch account using the Azure portal](https://docs.microsoft.com/azure/batch/batch-account-create-portal) for details.

## Upload files

To upload a folder of files run this command:
``` bash
azure batch file upload <path> <group>
```
| Parameter        | Description                                                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `<path>`         | File specification of the files to upload. Relative paths are resolved relative to the current directory.                                                                            |
| `<group>`        | Name for the file group that will be created in blob storage. <br/>When you view the file group in the Azure portal it will have the prefix `fgrp-` followed by the name specified here. |

For more information see the documentation on [input files](../../../inputFiles.md).

## Preparation

Fill out the parameter placeholders in `job.json`:

| Parameter        | Required  | Description                                                                                                                                                                                               |
| ---------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| testData         | Mandatory | The same name as you used for `<group>` when you uploaded files in the previous step.<br/>Note that this does not include the `fgrp-` prefix visible when you view blob storage through the Azure portal. |
| outputStorageUrl | Mandatory | A valid (non-expired) writable SAS key for blob storage (use the Azure portal to generate this).                                                                                                          |

To customize the job id or any of the details of the autopool, modify the appropriate details in `job.json`. These are not parameterized because they are not specified in the template file. 

## Run commands

To create your job, run the following command:
``` bash
azure batch job create --json-file job.json
```

This job uses an **autopool** which will automatically be deleted once the job reaches the Completed state. If the job never reaches the Completed state (e.g. when tasks are unable to run because of scheduling errors, or errors downloading files from storage), you will continue to be charged for the pool. In this case, you may want to use the [Azure portal](https://portal.azure.com) to manually delete the pool to ensure you're not billed unnecessarily.

## Monitor the job

You can use this command to monitor the tasks in the job and their progress:
``` bash
azure batch task list --job-id <jobid>`
```
You can also use the [Azure portal](https://portal.azure.com) or [Batch Explorer](https://github.com/Azure/azure-batch-samples/tree/master/CSharp/BatchExplorer) for monitoring.

## Structure of the sample 

| File            | Content                                                                                                                                                                                                                                                         |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `template.json` | Specifies an application template, containing all of the logic for the job we are going to run and any required parameters.                                                                                                                                     |
| `job.json`      | Defines the job to run by referencing the template file `template.json` and providing values for appropriate parameters. <br/> It also specifies the pool to use for the job, in this sample an auto pool containing **3** **STANDARD_D1_V2** virtual machines. |

## Troubleshooting

### "One of the specified Azure Blob(s) is not found"

If the preparation tasks for the job fail with the error *"One of the specified Azure Blob(s) is not found"*, verify that the resource file URLs specified for the file egress scripts are still correct (these URLs are dependent on the branch structure in the git repo for the XPlat CLI and may change without warning).

To check these URLs with the Azure Batch Portal, select the *Preparation Tasks* details page for your job then click the link next to *Resource Files*.  Another pane will open showing all the associated resource files and their URLs. Check that none of these return a 404 (not found) result in your browser.

If any of these files return a 404, you will need to point your installation to the correct files from github.com, as follows:

1. Go to [the github repository](https://github.com/Azure/azure-xplat-cli) (`https://github.com/Azure/azure-xplat-cli`)
2. Check the following branches (in order) to find one that contains the file `lib/commands/batch/fileegress/batchfileuploader.py`. 
    * master
    * dev
    * batch-beta
    * batch-beta-dev
3. Browse your installation of the XPlat CLI and open the file `lib/commands/batch/batch.templateUtil._js` in a Unicode-aware developers' text editor (such as [Visual Studio Code](https://code.visualstudio.com/), [Notepad++](https://notepad-plus-plus.org/) or [Vim](http://www.vim.org/)). 

4. Modify the assignment of `batchTemplateUtils.rootFileUploadUrl` (around line #34) to specify the branch you found above; the branch is the last part of the string.

5. Save the file and recreate your job from the command line.

To illustrate, this assignment specifies the branch `batch-beta`:
``` javascript
batchTemplateUtils.rootFileUploadUrl = 'https://raw.githubusercontent.com/Azure/azure-xplat-cli/batch-beta';
```
