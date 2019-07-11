.. :changelog:

SDK Release History
===================

6.0.1 (2019-06-20)
------------------

* Align to Python SDK for breaking changes to shared models

5.0.5 (2019-02-25)
------------------

* Fix bug in blobSource conversion to httpUrl

5.0.4 (2019-02-25)
------------------

* Fix bug where specifying a mergeTask in a template would cause task add failures.

5.0.3 (2019-02-19)
------------------

* Fix bug where blobSource was no longer an attribute of ExtendedResourceFile
* Improve test coverage

5.0.2 (2019-02-15)
------------------

* Fix bug where apiVersion became required

5.0.1 (2019-02-15)
------------------

* Fix bug where knack.get_logger was used instead of logging.getLogger

5.0.0 (2019-02-01)
------------------

* Align to Python SDK for breaking changes to shared models
* This also includes collapsing all models into one models file. Models should now be imported from the models namespace and not from their individual files.

4.0.2 (2018-10-06)
------------------

* Move `ExtendedTaskOperation` feature to standard Azure Batch SDK

4.0.1 (2018-10-04)
------------------

* Clean up code to meet Python standards

4.0.0 (2018-08-29)
------------------

* **Breaking** Model signatures are now using only keywords-arguments syntax. Each positional argument must be rewritten as a keyword argument.

3.1.2 (2018-08-22)
------------------

* Fix bug related to mis-configured endpoints for storage operations.

3.1.1 (2018-7-19)
------------------

* Enable using cloud shell AAD token for extension SDK
* Fix bug on using default thread count to submit tasks on the machine with odd number CPU cores

3.1.0 (2018-7-17)
------------------

* Align to Python SDK for shared models

3.0.0 (2018-6-20)
------------------

* Update add_collection function of ExtendedTaskOperations to retry failed requests due to server errors.
* Update add_collection function of ExtendedTaskOperations to track failed requests due to client errors and raise a CreateTasksErrorException if any occured.
* Elements of input template/json can be case insensitive.
* Escape in parameter json file doesn't need double escape.
* The callback of file operations include file name.

2.0.0 (2018-6-1)
------------------

* Rename the namespace to azext.batch

1.1.2 (2018-5-21)
------------------

* Update add_collection function of ExtendedTaskOperations to handle RequestBodyTooLarge error for well behaved tasks.
* Update add_collection function of ExtendedTaskOperations to enable degrees of parallelism.

1.1.1 (2018-4-10)
------------------

* Using azure-storage-blob as dependency
* Expand template only accept JSON dictionary object
* Minor bugs fix

1.0.1 (2017-10-10)
------------------

* Better support for unicode in Python 2.7

1.0.0 (2017-10-03)
------------------

* Support for Batch SDK version 4.0
* Added support for extended common_resource_files in MultiInstanceSettings
* Added support for native containers in tasks (including RepeatTask in a task factory)

0.2.0 (2017-07-29)
------------------

* Support for Batch SDK version 3.1 
* Fix bug with pool OS version detection
* Download from file group now supports prefix
* Support detection of Linux command using /bin/sh

0.1.1 (2017-07-10)
------------------

* Fix to support azure-cli-core v2.0.11


0.1.0 (2017-06-28)
------------------

* Initial preview release.

