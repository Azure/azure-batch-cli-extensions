Microsoft Azure Batch CLI Extensions for Windows, Mac and Linux
===============================================================

This project is a preview build of the Microsoft Azure command-line interface to demonstrate proposed features in Azure Batch.
For further details on the Azure CLI, please check the `official documentation <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>`_.

The purpose of this project is to allow customers to try out proposed Batch features and provide feedback to help shape the direction of the Batch service.
The features presented here may not be compatible with other Batch client SDKs and tools, nor will they necessarily be adopted into the core Batch service.

As these features are still in preview, they will be updated regularly, and refined based on customer feedback.
Unfortunately this may result in occasional breaking changes, though every effort will be made to keep this to a minimum.

Features
--------

`Input data upload to Batch linked storage accounts <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/inputFiles.md#input-file-upload>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A new command to allow a user to upload a set of files directly into the storage account linked to their Azure Batch account.

`Input data references using linked storage accounts <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/inputFiles.md#referencing-input-data>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Input data stored in linked storage under a file group can be simply referenced by a task by using some new ResourceFile properties. 

`Automatic persistence of task output files to a file group <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/outputFiles.md>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

When declaring task output files, you can now persist outputs to a named file group, without the need to generate a container SAS URL.

`Download job outputs from directly from storage <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/outputFiles.md#output-file-download>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A new command to allow a user to download job output files from a file group in the storage account linked to their Azure Batch account.

`Pool and job templates with parameterization <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/templates.md>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Templates allow pools and jobs to be defined in parameterized json files with a format inspired by ARM templates.

`Task factories for automatic task generation on job submission <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Task factories provide a way for a job and all its tasks to be created in one command instead
of calling `azure batch task create` for each task. There are currently three kinds of task factory:

* `Task Collection <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md#task-collection>`_ - tasks are explicitly defined as a part of the job
* `Parametric Sweep <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md#parametric-sweep>`_ - a set of tasks are created by substituting a range or sequence of values into a template 
* `Per File <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/taskFactories.md#task-per-file>`_ - a template task is replicated for each available input file 

`Split job configuration and management with reusable application templates <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/application-templates.md>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Application templates provide a way to partition the details of a job into two parts.

All of the details about how the job should be processed are moved into the **application template**, creating a reusable definition that is independent of a particular account. Application templates are parameterized to allow the processing to be customized without requiring modification of the template itself.

`Easy software installation via package managers <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/packages.md>`_
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Integration with existing 3rd party package managers to streamline the installation of applications. Currently the following package managers are supported:

* Chocolatey - for Windows
* APT - as used by some Linux distros including Ubuntu, Debian, and Fedora. 
* Yum - a package manager used by some Linux distros including  Red Hat Enterprise Linux, Fedora, CentOS. 


Samples
-------

Samples for all of the preview features can be found in `samples <https://github.com/Azure/azure-batch-cli-extensions/blob/master/samples>`_.

Installation
------------

In order to make use of these features, you must have the Azure CLI installed.
You can find futher instructions in the `official documentation <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>`_ and in the
`Azure CLI GitHub repository <https://github.com/azure/azure-cli>`_.

This extension package can be installed to supplement the existing Azure CLI Batch commands.
It can be installed using the CLI extension tools:

.. code-block:: bash

    $ az extension add --source [URL to latest release package]


Azure Batch account requirements
--------------------------------

In order to make use of the new features previewed here, you will need an Azure Batch account with a linked storage account.
For more information on this, see `Create an Azure Batch account using the Azure Portal <https://azure.microsoft.com/documentation/articles/batch-account-create-portal>`_.
