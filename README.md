# Microsoft Azure Batch Extensions

[![image](https://travis-ci.org/Azure/azure-batch-cli-extensions.svg?branch=master)](https://travis-ci.org/Azure/azure-batch-cli-extensions)

This project is a preview build of the Microsoft Azure command-line
interface to demonstrate proposed features in Azure Batch. For further
details on the Azure CLI, please check the [official
documentation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

The purpose of this project is to allow customers to try out proposed
Batch features and provide feedback to help shape the direction of the
Batch service. The features presented here may not be compatible with
other Batch client SDKs and tools, nor will they necessarily be adopted
into the core Batch service.

As these features are still in preview, they will be updated regularly,
and refined based on customer feedback. Unfortunately this may result in
occasional breaking changes, though every effort will be made to keep
this to a minimum.

## Features

  - [Input data upload to Batch linked storage
    accounts](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/inputFiles.md#input-file-upload)
    
    A new command to allow a user to upload a set of files directly into
    the storage account linked to their Azure Batch account.

  - [Input data references using linked storage
    accounts](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/inputFiles.md#referencing-input-data)
    
    Input data stored in linked storage under a file group can be simply
    referenced by a task by using some new ResourceFile properties.

  - [Automatic persistence of task output files to a file
    group](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/outputFiles.md)
    
    When declaring task output files, you can now persist outputs to a
    named file group, without the need to generate a container SAS URL.

  - [Download job outputs from directly from
    storage](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/outputFiles.md#output-file-download)
    
    A new command to allow a user to download job output files from a
    file group in the storage account linked to their Azure Batch
    account.

  - [Pool and job templates with
    parameterization](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/templates.md)
    
    Templates allow pools and jobs to be defined in parameterized json
    files with a format inspired by ARM templates.

  - [Task factories for automatic task generation on job
    submission](https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md)
    
    Task factories provide a way for a job and all its tasks to be
    created in one command instead of calling
    <span class="title-ref">azure batch task create</span> for each
    task. There are currently three kinds of task factory:
    
      - \`Task Collection
        \<<https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md#task-collectio>
