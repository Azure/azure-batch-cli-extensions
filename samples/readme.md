# Azure Batch Samples

Here are a collection of samples to demonstrate the new features in this Batch preview CLI.

## Hello World Samples

These samples use the new features in very simple ways to make it easier to see how these features might fit into your workflow.

### [Create pool and job](hello-world/create-pool-and-job)

Create a pool and then run a job with a single task. Both the pool and the job are defined using templates with hard coded values. 

Features used:

* [Pool and job templates with parameterization](../templates.md)
* [Task collection task factory](../taskFactories.md#task-collection)


### [Create pool and job with templates](hello-world/create-pool-and-job-with-templates)

Create a pool and then run a job with a single task. Both the pool and the job are defined using a parameterized templates. Parameter values used to fill out the templates are stored in separate files that are easy to modify as required.  

Features used:

* [Pool and job templates with parameterization](../templates.md)
* [Parametric sweep task factory](../taskFactories.md#parametric-sweep)
* [Task per file task factory](../taskFactories.md#task-per-file)


### [Task per file](hello-world/task-per-file)

Run a specific piece of processing independently across a set of files that are uploaded into storage. The job is specified as a template accepting parameters.

Features used:

* [Input data upload to Batch linked storage accounts](../inputFiles.md#input-file-upload)
* [Pool and job templates with parameterization](../templates.md)
* [Task per file task factory](../taskFactories.md#task-per-file)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)

### [Task per file with application template](hello-world/task-per-file-with-app-template)

Run a specific piece of processing independently across a set of files that are uploaded into storage. The actual processing involved is split out into a separate *application template*. The job itself references the template while specifying parameters, pool information and other management details. Application templates are intended to be flexible and reusable across a number of jobs.

Features used:

* [Split job configuration and management with reusable application templates](../application-templates.md)
* [Task per file task factory](../taskFactories.md#task-per-file)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)


## More Complex Samples

These samples show how to use the new features with real world applications.

### [FFmpeg](ffmpeg)

FFmpeg is an open-source command line tool for processing multimedia files. This is a sample demonstrating audio compression with Azure Batch on a large number of numerically-named files using a parametric sweep.

Features used:

* [Job template with parameterization](../templates.md)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)
* [Easy software installation via package managers](../packages.md)
* [Parametric sweep task factory](../taskFactories.md#parametric-sweep)
* [Task per file task factory](../taskFactories.md#task-per-file)

### [OCR](ocr)

OCR (Optical Character Recognition) is the process of extracting text from PDF images. This sample demonstrates the batch processing of PDF files.

Features used:

* [Pool and job templates with parameterization](../templates.md)
* [Parametric sweep task factory](../taskFactories.md#parametric-sweep)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)
* [Easy software installation via package managers](../packages.md)

### [MPI](mpi)

This sample demonstrates the batch run a MPI task with MultiInstanceSettings feature.

### [Blender](blender)

Blender is an open-source 3D content creation suite. This sample demonstrates distributed rendering on Azure Batch.  

Features used:

* [Job template with parameterization](../templates.md)
* [Parametric sweep task factory](../taskFactories.md#parametric-sweep)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)
* [Easy software installation via package managers](../packages.md)

### [Blender (Application Template)](blender-appTemplate) 

A variation of the [Blender](blender) sample that uses an application template to separate job definiton and management.

Features used:

* [Job template with parameterization](../templates.md)
* [Parametric sweep task factory](../taskFactories.md#parametric-sweep)
* [Automatic persistence of task output files to Azure Storage](../outputFiles.md)

### [Docker - Caffe](docker)

Caffe is an open-source deep learning framework. This sample demonstrates configuration of Caffe via Docker integration using Shipyard.


