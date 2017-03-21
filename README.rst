Microsoft Azure Batch CLI Extensions for Windows, Mac and Linux
===============================================================

.. image:: https://travis-ci.org/Azure/azure-batch-cli-extensions.svg?branch=master
 :target: https://travis-ci.org/Azure/azure-batch-cli-extensions

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

`Automatic persistence of task output files to Azure Storage <https://github.com/Azure/azure-batch-cli-extensions/blob/master/doc/outputFiles.md>`_
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

When adding a task, you can now declare a list of output files to be automatically uploaded to an Azure Storage container of your choice when the task completes.

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


Limitations
-----------

At this point, the following features will only work with Batch IaaS VMs using Linux (excluding Oracle Linux). IaaS VMs in Batch
are created with a VirtualMachineConfiguration as documented in the `Batch API documentation <https://msdn.microsoft.com/library/azure/dn820174.aspx#bk_vmconf>`_.

- Automatic task output-file persistence

Samples
-------

Samples for all of the preview features can be found in `samples <https://github.com/Azure/azure-batch-cli-extensions/blob/master/samples>`_.

Installation
------------

In order to make use of these features, you must have the Azure CLI installed.
You can find futher instructions in the `official documentation <https://docs.microsoft.com/en-us/cli/azure/install-azure-cli>`_ and in the
`Azure CLI GitHub repository <https://github.com/azure/azure-cli>`_.

This extension package can be installed to supplement the existing Azure CLI Batch commands.
It can be installed using the CLI component tools:

.. code-block:: bash

    $ az component update -add batch-extensions --allow-third-party


Azure Batch account requirements
--------------------------------

In order to make use of the new features previewed here, you will need an Azure Batch account with a linked storage account.
For more information on this, see `Create an Azure Batch account using the Azure Portal <https://azure.microsoft.com/documentation/articles/batch-account-create-portal>`_.

Contributing
------------

This project has adopted the `Microsoft Open Source Code of Conduct <https://opensource.microsoft.com/codeofconduct/>`_. For more information see the `Code of Conduct FAQ <https://opensource.microsoft.com/codeofconduct/faq/>`_ or contact `opencode@microsoft.com <mailto:opencode@microsoft.com>`_ with any additional questions or comments.

Developer Installation
----------------------

Preparing your machine
++++++++++++++++++++++
1.	Install Python 3.5.x from http://python.org. Please note that the version of Python that comes preinstalled on OSX is 2.7. 
2.	Clone your repository and check out the master branch.
3.	Create a new virtual environment “env” for Python 3.5 in the root of your clone. You can do this by running:

    **Windows**

    .. code-block:: bash

        python -m venv <clone root>\env

    **OSX/Ubuntu (bash)**

    .. code-block:: bash

        python –m venv <clone root>/env

4.	Activate the env virtual environment by running:

    **Windows**

    .. code-block:: bash

      <clone root>\env\scripts\activate.bat

    **OSX/Ubuntu (bash)**

    .. code-block:: bash

      . <clone root>/env/bin/activate

5.	Install the dependencies and load the command module as a local package using pip.

  .. code-block:: bash
  
    python scripts/dev_setup.py
