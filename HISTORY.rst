.. :changelog:

SDK Release History
===================

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

