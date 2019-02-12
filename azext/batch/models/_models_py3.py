import os
from .constants import *
import azure.batch.models as models
from msrest.serialization import Model


class TaskFactoryBase(Model):
    """A Task Factory for automatically adding a collection of tasks to a job on
    submission.

    :param merge_task: An optional additional task to be run after all the other
     generated tasks have completed successfully.
    :type merge_task: :class:`MergeTask <azext.batch.models.MergeTask>`
    """

    _validation = {
        'type': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'merge_task': {'key': 'mergeTask', 'type': 'MergeTask'}
    }

    _subtype_map = {
        'type': {'parametricSweep': 'ParametricSweepTaskFactory',
                 'taskPerFile': 'FileCollectionTaskFactory',
                 'taskCollection': 'TaskCollectionTaskFactory'}
    }

    def __init__(self, *, merge_task=None, **kwargs) -> None:
        super(TaskFactoryBase, self).__init__(**kwargs)
        self.merge_task = merge_task
        self.type = None


class PackageReferenceBase(Model):
    """A reference to a package to be installed on the compute nodes using
    a package manager.

    :param str id: The name of the package.
    :param str version: The version of the package to be installed. If omitted,
     the latest version (according to the package repository) will be installed.
    """

    _validation = {
        'type': {'required': True},
        'id': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
    }

    _subtype_map = {
        'type': {'aptPackage': 'AptPackageReference',
                 'chocolateyPackage': 'ChocolateyPackageReference',
                 'yumPackage': 'YumPackageReference'}
    }

    def __init__(self, *, id: str, version: str=None, **kwargs) -> None:
        super(PackageReferenceBase, self).__init__(**kwargs)
        self.type = None
        self.id = id
        self.version = version


class ApplicationTemplateInfo(Model):
    """A reference to an Azure Batch Application Template.

    :param str file_path: The path to an application template file. This can
     be a full path, or relative to the current working directory. Alternatively
     a relative directory can be supplied with the 'current_directory' argument.
     A ValueError will be raised if the supplied file path cannot be found.
    :param dict parameters: A dictory of parameter names and values to be
     subtituted into the application template.
    """

    _validation = {
        'file_path': {'required': True},
    }

    _attribute_map = {
        'file_path': {'key': 'filePath', 'type': 'str'},
        'parameters': {'key': 'parameters', 'type': 'object'},
    }

    def __init__(self, *, file_path: str, parameters: object=None, current_directory: str=".", **kwargs) -> None:
        super(ApplicationTemplateInfo, self).__init__(**kwargs)
        self.file_path = file_path
        if not os.path.isfile(self.file_path):
            current_directory = current_directory
            self.file_path = os.path.abspath(os.path.join(current_directory, str(self.file_path)))
        self.parameters = parameters

        # Rule: Template file must exist
        # (We do this in order to give a good diagnostic in the most common case, knowing that this is
        # technically a race condition because someone could delete the file between our check here and
        # reading the file later on. We expect such cases to be rare.)
        try:
            with open(self.file_path, 'r'):
                pass
        except EnvironmentError as error:
            raise ValueError("Unable to read the template '{}': {}".format(self.file_path, error))


class ApplicationTemplate(Model):
    """An Azure Batch Application Template.

    :param job_manager_task: Details of a Job Manager task to be launched when
     the job is started. If the job does not specify a Job Manager task, the
     user must explicitly add tasks to the job. If the job does specify a Job
     Manager task, the Batch service creates the Job Manager task when the job
     is created, and will try to schedule the Job Manager task before
     scheduling other tasks in the job. The Job Manager task's typical purpose
     is to control and/or monitor job execution, for example by deciding what
     additional tasks to run, determining when the work is complete, etc.
     (However, a Job Manager task is not restricted to these activities - it is
     a fully-fledged task in the system and perform whatever actions are
     required for the job.) For example, a Job Manager task might download a
     file specified as a parameter, analyze the contents of that file and
     submit additional tasks based on those contents.
    :type job_manager_task: :class:`JobManagerTask
     <azure.batch.models.JobManagerTask>`
    :param job_preparation_task: The Job Preparation task. If a job has a Job
     Preparation task, the Batch service will run the Job Preparation task on a
     compute node before starting any tasks of that job on that compute node.
    :type job_preparation_task: :class:`JobPreparationTask
     <azure.batch.models.JobPreparationTask>`
    :param job_release_task: The Job Release task. A Job Release task cannot
     be specified without also specifying a Job Preparation task for the job.
     The Batch service runs the Job Release task on the compute nodes that have
     run the Job Preparation task. The primary purpose of the Job Release task
     is to undo changes to compute nodes made by the Job Preparation task.
     Example activities include deleting local files, or shutting down services
     that were started as part of job preparation.
    :type job_release_task: :class:`JobReleaseTask
     <azure.batch.models.JobReleaseTask>`
    :param common_environment_settings: The list of common environment
     variable settings. These environment variables are set for all tasks in
     the job (including the Job Manager, Job Preparation and Job Release
     tasks). Individual tasks can override an environment setting specified
     here by specifying the same setting name with a different value.
    :type common_environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param on_all_tasks_complete: The action the Batch service should take
     when all tasks in the job are in the completed state. Note that if a job
     contains no tasks, then all tasks are considered complete. This option is
     therefore most commonly used with a Job Manager task; if you want to use
     automatic job termination without a Job Manager, you should initially set
     onAllTasksComplete to noAction and update the job properties to set
     onAllTasksComplete to terminateJob once you have finished adding tasks.
     Permitted values are: noAction - do nothing. The job remains active unless
     terminated or disabled by some other means. terminateJob - terminate the
     job. The job's terminateReason is set to 'AllTasksComplete'. The default
     is noAction. Possible values include: 'noAction', 'terminateJob'
    :type on_all_tasks_complete: str or :class:`OnAllTasksComplete
     <azure.batch.models.OnAllTasksComplete>`
    :param on_task_failure: The action the Batch service should take when any
     task in the job fails. A task is considered to have failed if has a
     failureInfo. A failureInfo is set if the task completes with a non-zero
     exit code after exhausting its retry count, or if there was an error
     starting the task, for example due to a resource file download error.
     noAction - do nothing. performExitOptionsJobAction - take the action
     associated with the task exit condition in the task's exitConditions
     collection. (This may still result in no action being taken, if that is
     what the task specifies.) The default is noAction. Possible values
     include: 'noAction', 'performExitOptionsJobAction'
    :type on_task_failure: str or :class:`OnTaskFailure
     <azure.batch.models.OnTaskFailure>`
    :param metadata: A list of name-value pairs associated with the job as
     metadata. The Batch service does not assign any meaning to metadata; it is
     solely for the use of user code.
    :type metadata: list of :class:`MetadataItem
     <azure.batch.models.MetadataItem>`
    :param uses_task_dependencies: Whether tasks in the job can define
     dependencies on each other. The default is false.
    :type uses_task_dependencies: bool
    :param task_factory: A task factory reference to automatically generate a set of
     tasks to be added to the job.
    :type task_factory: :class:`TaskFactoryBase
     <azext.batch.models.TaskFactoryBase>`
    """

    _attribute_map = {
        'job_manager_task': {'key': 'jobManagerTask', 'type': 'JobManagerTask'},
        'job_preparation_task': {'key': 'jobPreparationTask', 'type': 'JobPreparationTask'},
        'job_release_task': {'key': 'jobReleaseTask', 'type': 'JobReleaseTask'},
        'common_environment_settings': {'key': 'commonEnvironmentSettings', 'type': '[EnvironmentSetting]'},
        'on_all_tasks_complete': {'key': 'onAllTasksComplete', 'type': 'OnAllTasksComplete'},
        'on_task_failure': {'key': 'onTaskFailure', 'type': 'OnTaskFailure'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
        'uses_task_dependencies': {'key': 'usesTaskDependencies', 'type': 'bool'},
        'task_factory': {'key': 'taskFactory', 'type': 'TaskFactoryBase'},
    }

    def __init__(self, *, job_manager_task=None, job_preparation_task=None, job_release_task=None,
                 common_environment_settings=None, on_all_tasks_complete=None, on_task_failure=None,
                 metadata=None, uses_task_dependencies: bool=None, task_factory=None, **kwargs) -> None:
        super(ApplicationTemplate, self).__init__(**kwargs)
        self.job_manager_task = job_manager_task
        self.job_preparation_task = job_preparation_task
        self.job_release_task = job_release_task
        self.common_environment_settings = common_environment_settings
        self.on_all_tasks_complete = on_all_tasks_complete
        self.on_task_failure = on_task_failure
        self.metadata = metadata
        self.uses_task_dependencies = uses_task_dependencies
        self.task_factory = task_factory


class AptPackageReference(PackageReferenceBase):
    """A reference to a package to be installed using the APT package
    manager on a Linux node (apt-get).

    :param str id: The name of the package.
    :param str version: The version of the package to be installed. If omitted,
     the latest version (according to the package repository) will be installed.
    """

    _validation = {
        'type': {'required': True},
        'id': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
    }

    def __init__(self, *, id: str, version: str=None, **kwargs) -> None:
        super(AptPackageReference, self).__init__(id=id, version=version, **kwargs)
        self.type = 'aptPackage'


class AutoPoolSpecification(Model):
    """Specifies characteristics for a temporary 'auto pool'. The Batch service
    will create this auto pool when the job is submitted.

    :param auto_pool_id_prefix: A prefix to be added to the unique identifier
     when a pool is automatically created. The Batch service assigns each auto
     pool a unique identifier on creation. To distinguish between pools created
     for different purposes, you can specify this element to add a prefix to
     the ID that is assigned. The prefix can be up to 20 characters long.
    :type auto_pool_id_prefix: str
    :param pool_lifetime_option: The minimum lifetime of created auto pools,
     and how multiple jobs on a schedule are assigned to pools. When the pool
     lifetime is jobSchedule the pool exists for the lifetime of the job
     schedule. The Batch Service creates the pool when it creates the first job
     on the schedule. You may apply this option only to job schedules, not to
     jobs. When the pool lifetime is job the pool exists for the lifetime of
     the job to which it is dedicated. The Batch service creates the pool when
     it creates the job. If the 'job' option is applied to a job schedule, the
     Batch service creates a new auto pool for every job created on the
     schedule. Possible values include: 'jobSchedule', 'job'
    :type pool_lifetime_option: str or :class:`PoolLifetimeOption
     <azure.batch.models.PoolLifetimeOption>`
    :param keep_alive: Whether to keep an auto pool alive after its lifetime
     expires. If false, the Batch service deletes the pool once its lifetime
     (as determined by the poolLifetimeOption setting) expires; that is, when
     the job or job schedule completes. If true, the Batch service does not
     delete the pool automatically. It is up to the user to delete auto pools
     created with this option.
    :type keep_alive: bool
    :param pool: The pool specification for the auto pool.
    :type pool: :class:`PoolSpecification
     <azure.batch.models.PoolSpecification>`
    """

    _validation = {
        'pool_lifetime_option': {'required': True},
    }

    _attribute_map = {
        'auto_pool_id_prefix': {'key': 'autoPoolIdPrefix', 'type': 'str'},
        'pool_lifetime_option': {'key': 'poolLifetimeOption', 'type': 'PoolLifetimeOption'},
        'keep_alive': {'key': 'keepAlive', 'type': 'bool'},
        'pool': {'key': 'pool', 'type': 'ExtendedPoolSpecification'},
    }

    def __init__(self, *, pool_lifetime_option, auto_pool_id_prefix: str=None,
                 keep_alive: bool=None, pool=None, **kwargs) -> None:
        super(AutoPoolSpecification, self).__init__(**kwargs)
        self.auto_pool_id_prefix = auto_pool_id_prefix
        self.pool_lifetime_option = pool_lifetime_option
        self.keep_alive = keep_alive
        self.pool = pool


class ChocolateyPackageReference(PackageReferenceBase):
    """A reference to a package to be installed using the Chocolatey package
    manager on a Windows node.

    :param str id: The name of the package.
    :param str version: The version of the package to be installed. If omitted,
     the latest version (according to the package repository) will be installed.
    :param bool allow_empty_checksums: Whether Chocolatey will install packages
     without a checksum for validation. Default is false.
    """

    _validation = {
        'type': {'required': True},
        'id': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'allow_empty_checksums': {'key': 'allowEmptyChecksums', 'type': 'bool'}
    }

    def __init__(self, *, id: str, version: str=None, allow_empty_checksums: bool=None, **kwargs) -> None:
        super(ChocolateyPackageReference, self).__init__(id=id, version=version, **kwargs)
        self.allow_empty_checksums = allow_empty_checksums
        self.type = 'chocolateyPackage'


class ExtendedJobParameter(models.JobAddParameter):
    """An Azure Batch job to add.

    :param id: A string that uniquely identifies the job within the account.
     The ID can contain any combination of alphanumeric characters including
     hyphens and underscores, and cannot contain more than 64 characters. The
     ID is case-preserving and case-insensitive (that is, you may not have two
     IDs within an account that differ only by case).
    :type id: str
    :param display_name: The display name for the job. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param priority: The priority of the job. Priority values can range from
     -1000 to 1000, with -1000 being the lowest priority and 1000 being the
     highest priority. The default value is 0.
    :type priority: int
    :param constraints: The execution constraints for the job.
    :type constraints: :class:`JobConstraints
     <azure.batch.models.JobConstraints>`
    :param job_manager_task: Details of a Job Manager task to be launched when
     the job is started. If the job does not specify a Job Manager task, the
     user must explicitly add tasks to the job. If the job does specify a Job
     Manager task, the Batch service creates the Job Manager task when the job
     is created, and will try to schedule the Job Manager task before
     scheduling other tasks in the job. The Job Manager task's typical purpose
     is to control and/or monitor job execution, for example by deciding what
     additional tasks to run, determining when the work is complete, etc.
     (However, a Job Manager task is not restricted to these activities - it is
     a fully-fledged task in the system and perform whatever actions are
     required for the job.) For example, a Job Manager task might download a
     file specified as a parameter, analyze the contents of that file and
     submit additional tasks based on those contents.
    :type job_manager_task: :class:`JobManagerTask
     <azure.batch.models.JobManagerTask>`
    :param job_preparation_task: The Job Preparation task. If a job has a Job
     Preparation task, the Batch service will run the Job Preparation task on a
     compute node before starting any tasks of that job on that compute node.
    :type job_preparation_task: :class:`JobPreparationTask
     <azure.batch.models.JobPreparationTask>`
    :param job_release_task: The Job Release task. A Job Release task cannot
     be specified without also specifying a Job Preparation task for the job.
     The Batch service runs the Job Release task on the compute nodes that have
     run the Job Preparation task. The primary purpose of the Job Release task
     is to undo changes to compute nodes made by the Job Preparation task.
     Example activities include deleting local files, or shutting down services
     that were started as part of job preparation.
    :type job_release_task: :class:`JobReleaseTask
     <azure.batch.models.JobReleaseTask>`
    :param common_environment_settings: The list of common environment
     variable settings. These environment variables are set for all tasks in
     the job (including the Job Manager, Job Preparation and Job Release
     tasks). Individual tasks can override an environment setting specified
     here by specifying the same setting name with a different value.
    :type common_environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param pool_info: The pool on which the Batch service runs the job's
     tasks.
    :type pool_info: :class:`PoolInformation
     <azure.batch.models.PoolInformation>`
    :param on_all_tasks_complete: The action the Batch service should take
     when all tasks in the job are in the completed state. Note that if a job
     contains no tasks, then all tasks are considered complete. This option is
     therefore most commonly used with a Job Manager task; if you want to use
     automatic job termination without a Job Manager, you should initially set
     onAllTasksComplete to noAction and update the job properties to set
     onAllTasksComplete to terminateJob once you have finished adding tasks.
     Permitted values are: noAction - do nothing. The job remains active unless
     terminated or disabled by some other means. terminateJob - terminate the
     job. The job's terminateReason is set to 'AllTasksComplete'. The default
     is noAction. Possible values include: 'noAction', 'terminateJob'
    :type on_all_tasks_complete: str or :class:`OnAllTasksComplete
     <azure.batch.models.OnAllTasksComplete>`
    :param on_task_failure: The action the Batch service should take when any
     task in the job fails. A task is considered to have failed if has a
     failureInfo. A failureInfo is set if the task completes with a non-zero
     exit code after exhausting its retry count, or if there was an error
     starting the task, for example due to a resource file download error.
     noAction - do nothing. performExitOptionsJobAction - take the action
     associated with the task exit condition in the task's exitConditions
     collection. (This may still result in no action being taken, if that is
     what the task specifies.) The default is noAction. Possible values
     include: 'noAction', 'performExitOptionsJobAction'
    :type on_task_failure: str or :class:`OnTaskFailure
     <azure.batch.models.OnTaskFailure>`
    :param metadata: A list of name-value pairs associated with the job as
     metadata. The Batch service does not assign any meaning to metadata; it is
     solely for the use of user code.
    :type metadata: list of :class:`MetadataItem
     <azure.batch.models.MetadataItem>`
    :param uses_task_dependencies: Whether tasks in the job can define
     dependencies on each other. The default is false.
    :type uses_task_dependencies: bool
    :param task_factory: A task factory reference to automatically generate a set of
     tasks to be added to the job.
    :type task_factory: :class:`TaskFactoryBase
     <azext.batch.models.TaskFactoryBase>`
    :param application_template_info: A reference to an application template file to
     be expanded to complete the job specification. If supplied, the following arugments
     cannot also be supplied or they will be overwritten: 'job_manager_task',
    'common_environment_settings', 'uses_task_dependencies', 'on_all_tasks_complete',
    'on_task_failure', 'task_factory', 'job_preparation_task', 'job_release_task'.
    :type application_template_info: :class:`ApplicationTemplateInfo
     <azext.batch.models.ApplicationTemplateInfo>`
    """

    _validation = {
        'id': {'required': True},
        'pool_info': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'priority': {'key': 'priority', 'type': 'int'},
        'constraints': {'key': 'constraints', 'type': 'JobConstraints'},
        'job_manager_task': {'key': 'jobManagerTask', 'type': 'JobManagerTask'},
        'job_preparation_task': {'key': 'jobPreparationTask', 'type': 'JobPreparationTask'},
        'job_release_task': {'key': 'jobReleaseTask', 'type': 'JobReleaseTask'},
        'common_environment_settings': {'key': 'commonEnvironmentSettings', 'type': '[EnvironmentSetting]'},
        'pool_info': {'key': 'poolInfo', 'type': 'PoolInformation'},
        'on_all_tasks_complete': {'key': 'onAllTasksComplete', 'type': 'OnAllTasksComplete'},
        'on_task_failure': {'key': 'onTaskFailure', 'type': 'OnTaskFailure'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
        'uses_task_dependencies': {'key': 'usesTaskDependencies', 'type': 'bool'},
        'task_factory': {'key': 'taskFactory', 'type': 'TaskFactoryBase'},
        'application_template_info': {'key': 'applicationTemplateInfo', 'type': 'ApplicationTemplateInfo'}
    }

    def __init__(self, *, id: str, pool_info, display_name: str=None, priority: int=None, constraints=None,
                 job_manager_task=None, job_preparation_task=None, job_release_task=None,
                 common_environment_settings=None, on_all_tasks_complete=None, on_task_failure=None,
                 metadata=None, uses_task_dependencies: bool=None, task_factory=None,
                 application_template_info=None, **kwargs) -> None:
        super(ExtendedJobParameter, self).__init__(
            id=id,
            display_name=display_name,
            priority=priority,
            constraints=constraints,
            job_manager_task=job_manager_task,
            job_preparation_task=job_preparation_task,
            job_release_task=job_release_task,
            common_environment_settings=common_environment_settings,
            pool_info=pool_info,
            on_all_tasks_complete=on_all_tasks_complete,
            on_task_failure=on_task_failure,
            metadata=metadata,
            uses_task_dependencies=uses_task_dependencies,
            **kwargs)
        self.task_factory = task_factory
        self.application_template_info = application_template_info

        if self.application_template_info:
            # Rule: Jobs may not use properties reserved for template use
            reserved = [k for k, v in self.__dict__.items() \
                        if k in ATTRS_RESERVED_FOR_TEMPLATES and v is not None]
            if reserved:
                raise ValueError("Jobs using application templates may not use these "
                                 "properties: {}".format(', '.join(reserved)))


class ExtendedOutputFileDestination(Model):
    """The specification for where output files should be uploaded to on task
    completion.

    :param container: A location in Azure blob storage to which files are
     uploaded. This cannot be combined with auto_storage.
    :type container: :class:`OutputFileBlobContainerDestination
     <azure.batch.models.OutputFileBlobContainerDestination>`
    :param auto_storage: An auto-storage file group reference. This cannot be
     combined with container.
    :type auto_storage: :class:`OutputFileAutoStorageDestination
     <azext.batch.models.OutputFileAutoStorageDestination>`
    """

    _attribute_map = {
        'container': {'key': 'container', 'type': 'OutputFileBlobContainerDestination'},
        'auto_storage': {'key': 'autoStorage', 'type': 'OutputFileAutoStorageDestination'},
    }

    def __init__(self, *, container=None, auto_storage=None, **kwargs) -> None:
        super(ExtendedOutputFileDestination, self).__init__(**kwargs)
        if container and auto_storage:
            raise ValueError("Cannot specify both container and auto_storage.")
        self.container = container
        self.auto_storage = auto_storage


class ExtendedPoolParameter(models.PoolAddParameter):
    """A pool in the Azure Batch service to add.

    :param id: A string that uniquely identifies the pool within the account.
     The ID can contain any combination of alphanumeric characters including
     hyphens and underscores, and cannot contain more than 64 characters. The
     ID is case-preserving and case-insensitive (that is, you may not have two
     pool IDs within an account that differ only by case).
    :type id: str
    :param display_name: The display name for the pool. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param vm_size: The size of virtual machines in the pool. All virtual
     machines in a pool are the same size. For information about available
     sizes of virtual machines for Cloud Services pools (pools created with
     cloudServiceConfiguration), see Sizes for Cloud Services
     (http://azure.microsoft.com/documentation/articles/cloud-services-sizes-specs/).
     Batch supports all Cloud Services VM sizes except ExtraSmall, A1V2 and
     A2V2. For information about available VM sizes for pools using images from
     the Virtual Machines Marketplace (pools created with
     virtualMachineConfiguration) see Sizes for Virtual Machines (Linux)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-linux-sizes/)
     or Sizes for Virtual Machines (Windows)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-windows-sizes/).
     Batch supports all Azure VM sizes except STANDARD_A0 and those with
     premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series).
    :type vm_size: str
    :param cloud_service_configuration: The cloud service configuration for
     the pool. This property and virtualMachineConfiguration are mutually
     exclusive and one of the properties must be specified. This property
     cannot be specified if the Batch account was created with its
     poolAllocationMode property set to 'UserSubscription'.
    :type cloud_service_configuration: :class:`CloudServiceConfiguration
     <azure.batch.models.CloudServiceConfiguration>`
    :param virtual_machine_configuration: The virtual machine configuration
     for the pool. This property and cloudServiceConfiguration are mutually
     exclusive and one of the properties must be specified.
    :type virtual_machine_configuration: :class:`VirtualMachineConfiguration
     <azure.batch.models.VirtualMachineConfiguration>`
    :param resize_timeout: The timeout for allocation of compute nodes to the
     pool. This timeout applies only to manual scaling; it has no effect when
     enableAutoScale is set to true. The default value is 15 minutes. The
     minimum value is 5 minutes. If you specify a value less than 5 minutes,
     the Batch service returns an error; if you are calling the REST API
     directly, the HTTP status code is 400 (Bad Request).
    :type resize_timeout: timedelta
    :param target_dedicated_nodes: The desired number of dedicated compute
     nodes in the pool. This property must not be specified if enableAutoScale
     is set to true. If enableAutoScale is set to false, then you must set
     either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_dedicated_nodes: int
    :param target_low_priority_nodes: The desired number of low-priority
     compute nodes in the pool. This property must not be specified if
     enableAutoScale is set to true. If enableAutoScale is set to false, then
     you must set either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_low_priority_nodes: int
    :param enable_auto_scale: Whether the pool size should automatically
     adjust over time. If false, at least one of targetDedicateNodes and
     targetLowPriorityNodes must be specified. If true, the autoScaleFormula
     property is required and the pool automatically resizes according to the
     formula. The default value is false.
    :type enable_auto_scale: bool
    :param auto_scale_formula: A formula for the desired number of compute
     nodes in the pool. This property must not be specified if enableAutoScale
     is set to false. It is required if enableAutoScale is set to true. The
     formula is checked for validity before the pool is created. If the formula
     is not valid, the Batch service rejects the request with detailed error
     information. For more information about specifying this formula, see
     'Automatically scale compute nodes in an Azure Batch pool'
     (https://azure.microsoft.com/documentation/articles/batch-automatic-scaling/).
    :type auto_scale_formula: str
    :param auto_scale_evaluation_interval: The time interval at which to
     automatically adjust the pool size according to the autoscale formula. The
     default value is 15 minutes. The minimum and maximum value are 5 minutes
     and 168 hours respectively. If you specify a value less than 5 minutes or
     greater than 168 hours, the Batch service returns an error; if you are
     calling the REST API directly, the HTTP status code is 400 (Bad Request).
    :type auto_scale_evaluation_interval: timedelta
    :param enable_inter_node_communication: Whether the pool permits direct
     communication between nodes. Enabling inter-node communication limits the
     maximum size of the pool due to deployment restrictions on the nodes of
     the pool. This may result in the pool not reaching its desired size. The
     default value is false.
    :type enable_inter_node_communication: bool
    :param network_configuration: The network configuration for the pool.
    :type network_configuration: :class:`NetworkConfiguration
     <azure.batch.models.NetworkConfiguration>`
    :param start_task: A task specified to run on each compute node as it
     joins the pool. The task runs when the node is added to the pool or when
     the node is restarted.
    :type start_task: :class:`StartTask <azure.batch.models.StartTask>`
    :param certificate_references: The list of certificates to be installed on
     each compute node in the pool. For Windows compute nodes, the Batch
     service installs the certificates to the specified certificate store and
     location. For Linux compute nodes, the certificates are stored in a
     directory inside the task working directory and an environment variable
     AZ_BATCH_CERTIFICATES_DIR is supplied to the task to query for this
     location. For certificates with visibility of 'remoteUser', a 'certs'
     directory is created in the user's home directory (e.g.,
     /home/{user-name}/certs) and certificates are placed in that directory.
    :type certificate_references: list of :class:`CertificateReference
     <azure.batch.models.CertificateReference>`
    :param application_package_references: The list of application packages to
     be installed on each compute node in the pool.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param application_licenses: The list of application licenses the Batch
     service will make available on each compute node in the pool. The list of
     application licenses must be a subset of available Batch service
     application licenses. If a license is requested which is not supported,
     pool creation will fail.
    :type application_licenses: list of str
    :param max_tasks_per_node: The maximum number of tasks that can run
     concurrently on a single compute node in the pool. The default value is 1.
     The maximum value of this setting depends on the size of the compute nodes
     in the pool (the vmSize setting).
    :type max_tasks_per_node: int
    :param task_scheduling_policy: How tasks are distributed across compute
     nodes in a pool.
    :type task_scheduling_policy: :class:`TaskSchedulingPolicy
     <azure.batch.models.TaskSchedulingPolicy>`
    :param user_accounts: The list of user accounts to be created on each node
     in the pool.
    :type user_accounts: list of :class:`UserAccount
     <azure.batch.models.UserAccount>`
    :param metadata: A list of name-value pairs associated with the pool as
     metadata. The Batch service does not assign any meaning to metadata; it is
     solely for the use of user code.
    :type metadata: list of :class:`MetadataItem
     <azure.batch.models.MetadataItem>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'id': {'required': True},
        'vm_size': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'vm_size': {'key': 'vmSize', 'type': 'str'},
        'cloud_service_configuration': {'key': 'cloudServiceConfiguration',
                                        'type': 'CloudServiceConfiguration'},
        'virtual_machine_configuration': {'key': 'virtualMachineConfiguration',
                                          'type': 'VirtualMachineConfiguration'},
        'resize_timeout': {'key': 'resizeTimeout', 'type': 'duration'},
        'target_dedicated_nodes': {'key': 'targetDedicatedNodes', 'type': 'int'},
        'target_low_priority_nodes': {'key': 'targetLowPriorityNodes', 'type': 'int'},
        'enable_auto_scale': {'key': 'enableAutoScale', 'type': 'bool'},
        'auto_scale_formula': {'key': 'autoScaleFormula', 'type': 'str'},
        'auto_scale_evaluation_interval': {'key': 'autoScaleEvaluationInterval', 'type': 'duration'},
        'enable_inter_node_communication': {'key': 'enableInterNodeCommunication', 'type': 'bool'},
        'network_configuration': {'key': 'networkConfiguration', 'type': 'NetworkConfiguration'},
        'start_task': {'key': 'startTask', 'type': 'StartTask'},
        'certificate_references': {'key': 'certificateReferences', 'type': '[CertificateReference]'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'application_licenses': {'key': 'applicationLicenses', 'type': '[str]'},
        'max_tasks_per_node': {'key': 'maxTasksPerNode', 'type': 'int'},
        'task_scheduling_policy': {'key': 'taskSchedulingPolicy', 'type': 'TaskSchedulingPolicy'},
        'user_accounts': {'key': 'userAccounts', 'type': '[UserAccount]'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'}
    }

    def __init__(self, *, id: str, vm_size: str, display_name: str=None, cloud_service_configuration=None,
                 virtual_machine_configuration=None, resize_timeout=None, target_dedicated_nodes: int=None,
                 target_low_priority_nodes: int=None, enable_auto_scale: bool=None, auto_scale_formula: str=None,
                 auto_scale_evaluation_interval=None, enable_inter_node_communication: bool=None,
                 network_configuration=None, start_task=None, certificate_references=None,
                 application_package_references=None, application_licenses=None, max_tasks_per_node: int=None,
                 task_scheduling_policy=None, user_accounts=None, metadata=None, package_references=None,
                 **kwargs) -> None:
        super(ExtendedPoolParameter, self).__init__(
            id=id,
            display_name=display_name,
            vm_size=vm_size,
            cloud_service_configuration=cloud_service_configuration,
            virtual_machine_configuration=virtual_machine_configuration,
            resize_timeout=resize_timeout,
            target_dedicated_nodes=target_dedicated_nodes,
            target_low_priority_nodes=target_low_priority_nodes,
            enable_auto_scale=enable_auto_scale,
            auto_scale_formula=auto_scale_formula,
            auto_scale_evaluation_interval=auto_scale_evaluation_interval,
            enable_inter_node_communication=enable_inter_node_communication,
            network_configuration=network_configuration,
            start_task=start_task,
            certificate_references=certificate_references,
            application_package_references=application_package_references,
            application_licenses=application_licenses,
            max_tasks_per_node=max_tasks_per_node,
            task_scheduling_policy=task_scheduling_policy,
            user_accounts=user_accounts,
            metadata=metadata,
            **kwargs)
        self.package_references = package_references


class ExtendedPoolSpecification(models.PoolSpecification):
    """Specification for creating a new pool.

    :param display_name: The display name for the pool. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param vm_size: The size of the virtual machines in the pool. All virtual
     machines in a pool are the same size. For information about available
     sizes of virtual machines for Cloud Services pools (pools created with
     cloudServiceConfiguration), see Sizes for Cloud Services
     (http://azure.microsoft.com/documentation/articles/cloud-services-sizes-specs/).
     Batch supports all Cloud Services VM sizes except ExtraSmall, A1V2 and
     A2V2. For information about available VM sizes for pools using images from
     the Virtual Machines Marketplace (pools created with
     virtualMachineConfiguration) see Sizes for Virtual Machines (Linux)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-linux-sizes/)
     or Sizes for Virtual Machines (Windows)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-windows-sizes/).
     Batch supports all Azure VM sizes except STANDARD_A0 and those with
     premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series).
    :type vm_size: str
    :param cloud_service_configuration: The cloud service configuration for
     the pool. This property must be specified if the pool needs to be created
     with Azure PaaS VMs. This property and virtualMachineConfiguration are
     mutually exclusive and one of the properties must be specified. If neither
     is specified then the Batch service returns an error; if you are calling
     the REST API directly, the HTTP status code is 400 (Bad Request). This
     property cannot be specified if the Batch account was created with its
     poolAllocationMode property set to 'UserSubscription'.
    :type cloud_service_configuration: :class:`CloudServiceConfiguration
     <azure.batch.models.CloudServiceConfiguration>`
    :param virtual_machine_configuration: The virtual machine configuration
     for the pool. This property must be specified if the pool needs to be
     created with Azure IaaS VMs. This property and cloudServiceConfiguration
     are mutually exclusive and one of the properties must be specified. If
     neither is specified then the Batch service returns an error; if you are
     calling the REST API directly, the HTTP status code is 400 (Bad Request).
    :type virtual_machine_configuration: :class:`VirtualMachineConfiguration
     <azure.batch.models.VirtualMachineConfiguration>`
    :param max_tasks_per_node: The maximum number of tasks that can run
     concurrently on a single compute node in the pool. The default value is 1.
     The maximum value of this setting depends on the size of the compute nodes
     in the pool (the vmSize setting).
    :type max_tasks_per_node: int
    :param task_scheduling_policy: How tasks are distributed across compute
     nodes in a pool.
    :type task_scheduling_policy: :class:`TaskSchedulingPolicy
     <azure.batch.models.TaskSchedulingPolicy>`
    :param resize_timeout: The timeout for allocation of compute nodes to the
     pool. This timeout applies only to manual scaling; it has no effect when
     enableAutoScale is set to true. The default value is 15 minutes. The
     minimum value is 5 minutes. If you specify a value less than 5 minutes,
     the Batch service rejects the request with an error; if you are calling
     the REST API directly, the HTTP status code is 400 (Bad Request).
    :type resize_timeout: timedelta
    :param target_dedicated_nodes: The desired number of dedicated compute
     nodes in the pool. This property must not be specified if enableAutoScale
     is set to true. If enableAutoScale is set to false, then you must set
     either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_dedicated_nodes: int
    :param target_low_priority_nodes: The desired number of low-priority
     compute nodes in the pool. This property must not be specified if
     enableAutoScale is set to true. If enableAutoScale is set to false, then
     you must set either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_low_priority_nodes: int
    :param enable_auto_scale: Whether the pool size should automatically
     adjust over time. If false, the targetDedicated element is required. If
     true, the autoScaleFormula element is required. The pool automatically
     resizes according to the formula. The default value is false.
    :type enable_auto_scale: bool
    :param auto_scale_formula: The formula for the desired number of compute
     nodes in the pool. This property must not be specified if enableAutoScale
     is set to false. It is required if enableAutoScale is set to true. The
     formula is checked for validity before the pool is created. If the formula
     is not valid, the Batch service rejects the request with detailed error
     information.
    :type auto_scale_formula: str
    :param auto_scale_evaluation_interval: The time interval at which to
     automatically adjust the pool size according to the autoscale formula. The
     default value is 15 minutes. The minimum and maximum value are 5 minutes
     and 168 hours respectively. If you specify a value less than 5 minutes or
     greater than 168 hours, the Batch service rejects the request with an
     invalid property value error; if you are calling the REST API directly,
     the HTTP status code is 400 (Bad Request).
    :type auto_scale_evaluation_interval: timedelta
    :param enable_inter_node_communication: Whether the pool permits direct
     communication between nodes. Enabling inter-node communication limits the
     maximum size of the pool due to deployment restrictions on the nodes of
     the pool. This may result in the pool not reaching its desired size. The
     default value is false.
    :type enable_inter_node_communication: bool
    :param network_configuration: The network configuration for the pool.
    :type network_configuration: :class:`NetworkConfiguration
     <azure.batch.models.NetworkConfiguration>`
    :param start_task: A task to run on each compute node as it joins the
     pool. The task runs when the node is added to the pool or when the node is
     restarted.
    :type start_task: :class:`StartTask <azure.batch.models.StartTask>`
    :param certificate_references: A list of certificates to be installed on
     each compute node in the pool. For Windows compute nodes, the Batch
     service installs the certificates to the specified certificate store and
     location. For Linux compute nodes, the certificates are stored in a
     directory inside the task working directory and an environment variable
     AZ_BATCH_CERTIFICATES_DIR is supplied to the task to query for this
     location. For certificates with visibility of 'remoteUser', a 'certs'
     directory is created in the user's home directory (e.g.,
     /home/{user-name}/certs) and certificates are placed in that directory.
    :type certificate_references: list of :class:`CertificateReference
     <azure.batch.models.CertificateReference>`
    :param application_package_references: The list of application packages to
     be installed on each compute node in the pool.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param application_licenses: The list of application licenses the Batch
     service will make available on each compute node in the pool. The list of
     application licenses must be a subset of available Batch service
     application licenses. If a license is requested which is not supported,
     pool creation will fail.
    :type application_licenses: list of str
    :param user_accounts: The list of user accounts to be created on each node
     in the pool.
    :type user_accounts: list of :class:`UserAccount
     <azure.batch.models.UserAccount>`
    :param metadata: A list of name-value pairs associated with the pool as
     metadata. The Batch service does not assign any meaning to metadata; it is
     solely for the use of user code.
    :type metadata: list of :class:`MetadataItem
     <azure.batch.models.MetadataItem>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'vm_size': {'required': True},
    }

    _attribute_map = {
        'display_name': {'key': 'displayName', 'type': 'str'},
        'vm_size': {'key': 'vmSize', 'type': 'str'},
        'cloud_service_configuration': {'key': 'cloudServiceConfiguration',
                                        'type': 'CloudServiceConfiguration'},
        'virtual_machine_configuration': {'key': 'virtualMachineConfiguration',
                                          'type': 'VirtualMachineConfiguration'},
        'max_tasks_per_node': {'key': 'maxTasksPerNode', 'type': 'int'},
        'task_scheduling_policy': {'key': 'taskSchedulingPolicy', 'type': 'TaskSchedulingPolicy'},
        'resize_timeout': {'key': 'resizeTimeout', 'type': 'duration'},
        'target_dedicated_nodes': {'key': 'targetDedicatedNodes', 'type': 'int'},
        'target_low_priority_nodes': {'key': 'targetLowPriorityNodes', 'type': 'int'},
        'enable_auto_scale': {'key': 'enableAutoScale', 'type': 'bool'},
        'auto_scale_formula': {'key': 'autoScaleFormula', 'type': 'str'},
        'auto_scale_evaluation_interval': {'key': 'autoScaleEvaluationInterval', 'type': 'duration'},
        'enable_inter_node_communication': {'key': 'enableInterNodeCommunication', 'type': 'bool'},
        'network_configuration': {'key': 'networkConfiguration', 'type': 'NetworkConfiguration'},
        'start_task': {'key': 'startTask', 'type': 'StartTask'},
        'certificate_references': {'key': 'certificateReferences', 'type': '[CertificateReference]'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'application_licenses': {'key': 'applicationLicenses', 'type': '[str]'},
        'user_accounts': {'key': 'userAccounts', 'type': '[UserAccount]'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'}
    }

    def __init__(self, *, vm_size: str, display_name: str=None, cloud_service_configuration=None,
                 virtual_machine_configuration=None, max_tasks_per_node: int=None, task_scheduling_policy=None,
                 resize_timeout=None, target_dedicated_nodes: int=None, target_low_priority_nodes: int=None,
                 enable_auto_scale: bool=None, auto_scale_formula: str=None, auto_scale_evaluation_interval=None,
                 enable_inter_node_communication: bool=None, network_configuration=None, start_task=None,
                 certificate_references=None, application_package_references=None, application_licenses=None,
                 user_accounts=None, metadata=None, package_references=None, **kwargs) -> None:
        super(ExtendedPoolSpecification, self).__init__(
            display_name=display_name,
            vm_size=vm_size,
            cloud_service_configuration=cloud_service_configuration,
            virtual_machine_configuration=virtual_machine_configuration,
            max_tasks_per_node=max_tasks_per_node,
            task_scheduling_policy=task_scheduling_policy,
            resize_timeout=resize_timeout,
            target_dedicated_nodes=target_dedicated_nodes,
            target_low_priority_nodes=target_low_priority_nodes,
            enable_auto_scale=enable_auto_scale,
            auto_scale_formula=auto_scale_formula,
            auto_scale_evaluation_interval=auto_scale_evaluation_interval,
            enable_inter_node_communication=enable_inter_node_communication,
            network_configuration=network_configuration,
            start_task=start_task,
            certificate_references=certificate_references,
            application_package_references=application_package_references,
            application_licenses=application_licenses,
            user_accounts=user_accounts,
            metadata=metadata,
            **kwargs)
        self.package_references = package_references


class ExtendedResourceFile(models.ResourceFile):
    """A file to be downloaded from Azure blob storage to a compute node.

    :param http_url: The URL of the file within Azure Blob Storage. This
     URL must be readable using anonymous access; that is, the Batch service
     does not present any credentials when downloading the blob. There are two
     ways to get such a URL for a blob in Azure storage: include a Shared
     Access Signature (SAS) granting read permissions on the blob, or set the
     ACL for the blob or its container to allow public access.
    :type http_url: str
    :param auto_storage_container_name: The storage container name in the auto
    storage account. The autoStorageContainerName, storageContainerUrl and
    httpUrl properties are mutually exclusive and one of them must be specified.
    :type auto_storage_container_name: str
    :param storage_container_url: The URL of the blob container within Azure
    Blob Storage. The autoStorageContainerName, storageContainerUrl and httpUrl
    properties are mutually exclusive and one of them must be specified. This
    URL must be readable and listable using anonymous access; that is, the
    Batch service does not present any credentials when downloading blobs from
    the container. There are two ways to get such a URL for a container in
    Azure storage: include a Shared Access Signature (SAS) granting read and
    list permissions on the container, or set the ACL for the container to
    allow public access.
    :type storage_container_url: str
    :param blob_prefix: The blob prefix to use when downloading blobs from an
    Azure Storage container. Only the blobs whose names begin with the specified
    prefix will be downloaded. The property is valid only when
    autoStorageContainerName or storageContainerUrl is used. This prefix can be
    a partial filename or a subdirectory. If a prefix is not specified, all the
    files in the container will be downloaded.
    :type blob_prefix: str
    :param file_path: The location on the compute node to which to download
     the file, relative to the task's working directory. If using a file group
     source that references more than one file, this will be considered the name
     of a directory, otherwise it will be treated as the destination file name.
    :type file_path: str
    :param file_mode: The file permission mode attribute in octal format. This
     property applies only to files being downloaded to Linux compute nodes. It
     will be ignored if it is specified for a resourceFile which will be
     downloaded to a Windows node. If this property is not specified for a
     Linux node, then a default value of 0770 is applied to the file.
     If using a file group source that references more than one file, this will be
     applied to all files in the group.
    :type file_mode: str
    :param source: A file source reference which could include a collection of files from
     a Azure Storage container or an auto-storage file group.
    :type source: :class:`FileSource
     <azext.batch.models.FileSource>`
    """

    _attribute_map = {
        'http_url': {'key': 'httpUrl', 'type': 'str'},
        'auto_storage_container_name': {'key': 'autoStorageContainerName', 'type': 'str'},
        'blob_prefix': {'key': 'blobPrefix', 'type': 'str'},
        'storage_container_url': {'key': 'storageContainerUrl', 'type': 'str'},
        'file_path': {'key': 'filePath', 'type': 'str'},
        'file_mode': {'key': 'fileMode', 'type': 'str'},
        'source': {'key': 'source', 'type': 'FileSource'}
    }

    def __init__(self,
                 *,
                 http_url: str=None,
                 auto_storage_container_name: str=None,
                 storage_container_url: str=None,
                 blob_prefix: str=None,
                 file_path: str=None,
                 file_mode: str=None,
                 source=None, **kwargs) -> None:
        super(ExtendedResourceFile, self).__init__(
            http_url=http_url,
            auto_storage_container_name=auto_storage_container_name,
            storage_container_url=storage_container_url,
            blob_prefix=blob_prefix,
            file_path=file_path,
            file_mode=file_mode,
            **kwargs)
        self.source = source


class ExtendedTaskParameter(models.TaskAddParameter):
    """An Azure Batch task to add.

    :param id: A string that uniquely identifies the task within the job. The
     ID can contain any combination of alphanumeric characters including
     hyphens and underscores, and cannot contain more than 64 characters. The
     ID is case-preserving and case-insensitive (that is, you may not have two
     IDs within a job that differ only by case).
    :type id: str
    :param display_name: A display name for the task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: The command line of the task. For multi-instance
     tasks, the command line is executed as the primary task, after the primary
     task and all subtasks have finished executing the coordination command
     line. The command line does not run under a shell, and therefore cannot
     take advantage of shell features such as environment variable expansion.
     If you want to take advantage of such features, you should invoke the
     shell in the command line, for example using "cmd /c MyCommand" in Windows
     or "/bin/sh -c MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     task runs. If the pool that will run this task has containerConfiguration
     set, this must be set as well. If the pool that will run this task doesn't
     have containerConfiguration set, this must not be set. When this is
     specified, all directories recursively below the AZ_BATCH_NODE_ROOT_DIR
     (the root of Azure Batch directories on the node) are mapped into the
     container, all task environment variables are mapped into the container,
     and the task command line is executed in the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param exit_conditions: How the Batch service should respond when the task
     completes.
    :type exit_conditions: :class:`ExitConditions
     <azure.batch.models.ExitConditions>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. For
     multi-instance tasks, the resource files will only be downloaded to the
     compute node on which the primary task is executed.
    :type resource_files: list of :class:`ResourceFile
     <azure.batch.models.ResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param affinity_info: A locality hint that can be used by the Batch
     service to select a compute node on which to start the new task.
    :type affinity_info: :class:`AffinityInformation
     <azure.batch.models.AffinityInformation>`
    :param constraints: The execution constraints that apply to this task. If
     you do not specify constraints, the maxTaskRetryCount is the
     maxTaskRetryCount specified for the job, and the maxWallClockTime and
     retentionTime are infinite.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param user_identity: The user identity under which the task runs. If
     omitted, the task runs as a non-administrative user unique to the task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param multi_instance_settings: An object that indicates that the task is
     a multi-instance task, and contains information about how to run the
     multi-instance task.
    :type multi_instance_settings: :class:`MultiInstanceSettings
     <azure.batch.models.MultiInstanceSettings>`
    :param depends_on: The tasks that this task depends on. This task will not
     be scheduled until all tasks that it depends on have completed
     successfully. If any of those tasks fail and exhaust their retry counts,
     this task will never be scheduled. If the job does not have
     usesTaskDependencies set to true, and this element is present, the request
     fails with error code TaskDependenciesNotSpecifiedOnJob.
    :type depends_on: :class:`TaskDependencies
     <azure.batch.models.TaskDependencies>`
    :param application_package_references: A list of application packages that
     the Batch service will deploy to the compute node before running the
     command line. Application packages are downloaded and deployed to a shared
     directory, not the task working directory. Therefore, if a referenced
     package is already on the compute node, and is up to date, then it is not
     re-downloaded; the existing copy on the compute node is used. If a
     referenced application package cannot be installed, for example because
     the package has been deleted or because download failed, the task fails.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param authentication_token_settings: The settings for an authentication
     token that the task can use to perform Batch service operations. If this
     property is set, the Batch service provides the task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the task can carry out using the token depend on the settings. For
     example, a task can request job permissions in order to add other tasks to
     the job, or check the status of the job or of other tasks under the job.
    :type authentication_token_settings: :class:`AuthenticationTokenSettings
     <azure.batch.models.AuthenticationTokenSettings>`
    :param output_files: A list of files that the Batch service will upload
     from the compute node after running the command line. For multi-instance
     tasks, the files will only be uploaded from the compute node on which the
     primary task is executed.
    :type output_files: list of :class:`OutputFile
     <azext.batch.models.OutputFile>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'id': {'required': True},
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'multi_instance_settings': {'key': 'multiInstanceSettings', 'type': 'MultiInstanceSettings'},
        'depends_on': {'key': 'dependsOn', 'type': 'TaskDependencies'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'}
    }

    def __init__(self, *, id: str, command_line: str, display_name: str=None, container_settings=None,
                 exit_conditions=None, resource_files=None, output_files=None, environment_settings=None,
                 affinity_info=None, constraints=None, user_identity=None,
                 multi_instance_settings=None, depends_on=None,
                 application_package_references=None, authentication_token_settings=None,
                 package_references=None, **kwargs) -> None:
        super(ExtendedTaskParameter, self).__init__(
            id=id,
            display_name=display_name,
            command_line=command_line,
            container_settings=container_settings,
            exit_conditions=exit_conditions,
            resource_files=resource_files,
            output_files=output_files,
            environment_settings=environment_settings,
            affinity_info=affinity_info,
            constraints=constraints,
            user_identity=user_identity,
            multi_instance_settings=multi_instance_settings,
            depends_on=depends_on,
            application_package_references=application_package_references,
            authentication_token_settings=authentication_token_settings,
            **kwargs)
        self.package_references = package_references


class FileCollectionTaskFactory(TaskFactoryBase):
    """A Task Factory for generating a set of tasks based on the contents
    of an Azure Storage container or auto-storage file group. One task
    will be generated per input file, and automatically added to the job.

    :param source: The input file source from which the tasks will be generated.
    :type source: :class:`FileSource <azext.batch.models.FileSource>`
    :param repeat_task: The task template the will be used to generate each task.
    :type repeat_task: :class:`RepeatTask <azext.batch.models.RepeatTask>`
    :param merge_task: An optional additional task to be run after all the other
     generated tasks have completed successfully.
    :type merge_task: :class:`MergeTask <azext.batch.models.MergeTask>`
    """

    _validation = {
        'type': {'required': True},
        'source': {'required': True},
        'repeat_task': {'required': True}
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'source': {'key': 'source', 'type': 'FileSource'},
        'repeat_task': {'key': 'repeatTask', 'type': 'RepeatTask'},
        'merge_task': {'key': 'mergeTask', 'type': 'MergeTask'}
    }

    def __init__(self, *, source: str, repeat_task, merge_task=None, **kwargs) -> None:
        super(FileCollectionTaskFactory, self).__init__(
            merge_task=merge_task, **kwargs)
        self.source = source
        self.repeat_task = repeat_task
        self.type = 'taskPerFile'


class FileSource(Model):
    """A source of input files to be downloaded onto a compute node.

    :param str file_group: The name of an auto-storage file group.
    :param str url: The URL of a file to be downloaded.
    :param str container_url: The SAS URL of an Azure Storage container.
    :param str prefix: The filename prefix or subdirectory of input files
     in either an auto-storage file group or container. Will be ignored if
     conbined with url.
    """

    _attribute_map = {
        'file_group': {'key': 'fileGroup', 'type': 'str'},
        'url': {'key': 'url', 'type': 'str'},
        'container_url': {'key': 'containerUrl', 'type': 'str'},
        'prefix': {'key': 'prefix', 'type': 'str'},
    }

    def __init__(self, *, file_group: str=None, url: str=None,
                 container_url: str=None, prefix: str=None, **kwargs) -> None:
        super(FileSource, self).__init__(**kwargs)
        self.file_group = file_group
        self.url = url
        self.container_url = container_url
        self.prefix = prefix


class JobManagerTask(Model):
    """Specifies details of a Job Manager task.

    The Job Manager task is automatically started when the job is created. The
    Batch service tries to schedule the Job Manager task before any other tasks
    in the job. When shrinking a pool, the Batch service tries to preserve
    compute nodes where Job Manager tasks are running for as long as possible
    (that is, nodes running 'normal' tasks are removed before nodes running Job
    Manager tasks). When a Job Manager task fails and needs to be restarted,
    the system tries to schedule it at the highest priority. If there are no
    idle nodes available, the system may terminate one of the running tasks in
    the pool and return it to the queue in order to make room for the Job
    Manager task to restart. Note that a Job Manager task in one job does not
    have priority over tasks in other jobs. Across jobs, only job level
    priorities are observed. For example, if a Job Manager in a priority 0 job
    needs to be restarted, it will not displace tasks of a priority 1 job.

    :param id: A string that uniquely identifies the Job Manager task within
     the job. The ID can contain any combination of alphanumeric characters
     including hyphens and underscores and cannot contain more than 64
     characters.
    :type id: str
    :param display_name: The display name of the Job Manager task. It need not
     be unique and can contain any Unicode characters up to a maximum length of
     1024.
    :type display_name: str
    :param command_line: The command line of the Job Manager task. The command
     line does not run under a shell, and therefore cannot take advantage of
     shell features such as environment variable expansion. If you want to take
     advantage of such features, you should invoke the shell in the command
     line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c
     MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     Job Manager task runs. If the pool that will run this task has
     containerConfiguration set, this must be set as well. If the pool that
     will run this task doesn't have containerConfiguration set, this must not
     be set. When this is specified, all directories recursively below the
     AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch directories on the node)
     are mapped into the container, all task environment variables are mapped
     into the container, and the task command line is executed in the
     container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. Files listed
     under this element are located in the task's working directory.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param output_files: A list of files that the Batch service will upload
     from the compute node after running the command line. For multi-instance
     tasks, the files will only be uploaded from the compute node on which the
     primary task is executed.
    :type output_files: list of :class:`OutputFile
     <azure.batch.models.OutputFile>`
    :param environment_settings: A list of environment variable settings for
     the Job Manager task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param constraints: Constraints that apply to the Job Manager task.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param kill_job_on_completion: Whether completion of the Job Manager task
     signifies completion of the entire job. If true, when the Job Manager task
     completes, the Batch service marks the job as complete. If any tasks are
     still running at this time (other than Job Release), those tasks are
     terminated. If false, the completion of the Job Manager task does not
     affect the job status. In this case, you should either use the
     onAllTasksComplete attribute to terminate the job, or have a client or
     user terminate the job explicitly. An example of this is if the Job
     Manager creates a set of tasks but then takes no further role in their
     execution. The default value is true. If you are using the
     onAllTasksComplete and onTaskFailure attributes to control job lifetime,
     and using the Job Manager task only to create the tasks for the job (not
     to monitor progress), then it is important to set killJobOnCompletion to
     false.
    :type kill_job_on_completion: bool
    :param user_identity: The user identity under which the Job Manager task
     runs. If omitted, the task runs as a non-administrative user unique to the
     task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param run_exclusive: Whether the Job Manager task requires exclusive use
     of the compute node where it runs. If true, no other tasks will run on the
     same compute node for as long as the Job Manager is running. If false,
     other tasks can run simultaneously with the Job Manager on a compute node.
     The Job Manager task counts normally against the node's concurrent task
     limit, so this is only relevant if the node allows multiple concurrent
     tasks. The default value is true.
    :type run_exclusive: bool
    :param application_package_references: A list of application packages that
     the Batch service will deploy to the compute node before running the
     command line. Application packages are downloaded and deployed to a shared
     directory, not the task working directory. Therefore, if a referenced
     package is already on the compute node, and is up to date, then it is not
     re-downloaded; the existing copy on the compute node is used. If a
     referenced application package cannot be installed, for example because
     the package has been deleted or because download failed, the task fails.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param authentication_token_settings: The settings for an authentication
     token that the task can use to perform Batch service operations. If this
     property is set, the Batch service provides the task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the task can carry out using the token depend on the settings. For
     example, a task can request job permissions in order to add other tasks to
     the job, or check the status of the job or of other tasks under the job.
    :type authentication_token_settings: :class:`AuthenticationTokenSettings
     <azure.batch.models.AuthenticationTokenSettings>`
    :param allow_low_priority_node: Whether the Job Manager task may run on a
     low-priority compute node. The default value is false.
    :type allow_low_priority_node: bool
    """

    _validation = {
        'id': {'required': True},
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'kill_job_on_completion': {'key': 'killJobOnCompletion', 'type': 'bool'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'run_exclusive': {'key': 'runExclusive', 'type': 'bool'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'allow_low_priority_node': {'key': 'allowLowPriorityNode', 'type': 'bool'},
    }

    def __init__(self, *, id: str, command_line: str, display_name: str=None, container_settings=None,
                 resource_files=None, output_files=None, environment_settings=None, constraints=None,
                 kill_job_on_completion: bool=None, user_identity=None, run_exclusive: bool=None,
                 application_package_references=None, authentication_token_settings=None,
                 allow_low_priority_node: bool=None, **kwargs) -> None:
        super(JobManagerTask, self).__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.command_line = command_line
        self.container_settings = container_settings
        self.resource_files = resource_files
        self.output_files = output_files
        self.environment_settings = environment_settings
        self.constraints = constraints
        self.kill_job_on_completion = kill_job_on_completion
        self.user_identity = user_identity
        self.run_exclusive = run_exclusive
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
        self.allow_low_priority_node = allow_low_priority_node


class JobPreparationTask(Model):
    """A Job Preparation task to run before any tasks of the job on any given
    compute node.

    You can use Job Preparation to prepare a compute node to run tasks for the
    job. Activities commonly performed in Job Preparation include: Downloading
    common resource files used by all the tasks in the job. The Job Preparation
    task can download these common resource files to the shared location on the
    compute node. (AZ_BATCH_NODE_ROOT_DIR\\shared), or starting a local service
    on the compute node so that all tasks of that job can communicate with it.
    If the Job Preparation task fails (that is, exhausts its retry count before
    exiting with exit code 0), Batch will not run tasks of this job on the
    compute node. The node remains ineligible to run tasks of this job until it
    is reimaged. The node remains active and can be used for other jobs. The
    Job Preparation task can run multiple times on the same compute node.
    Therefore, you should write the Job Preparation task to handle
    re-execution. If the compute node is rebooted, the Job Preparation task is
    run again on the node before scheduling any other task of the job, if
    rerunOnNodeRebootAfterSuccess is true or if the Job Preparation task did
    not previously complete. If the compute node is reimaged, the Job
    Preparation task is run again before scheduling any task of the job.

    :param id: A string that uniquely identifies the Job Preparation task
     within the job. The ID can contain any combination of alphanumeric
     characters including hyphens and underscores and cannot contain more than
     64 characters. If you do not specify this property, the Batch service
     assigns a default value of 'jobpreparation'. No other task in the job can
     have the same ID as the Job Preparation task. If you try to submit a task
     with the same ID, the Batch service rejects the request with error code
     TaskIdSameAsJobPreparationTask; if you are calling the REST API directly,
     the HTTP status code is 409 (Conflict).
    :type id: str
    :param command_line: The command line of the Job Preparation task. The
     command line does not run under a shell, and therefore cannot take
     advantage of shell features such as environment variable expansion. If you
     want to take advantage of such features, you should invoke the shell in
     the command line, for example using "cmd /c MyCommand" in Windows or
     "/bin/sh -c MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     Job Preparation task runs. When this is specified, all directories
     recursively below the AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch
     directories on the node) are mapped into the container, all task
     environment variables are mapped into the container, and the task command
     line is executed in the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. Files listed
     under this element are located in the task's working directory.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the Job Preparation task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param constraints: Constraints that apply to the Job Preparation task.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param wait_for_success: Whether the Batch service should wait for the Job
     Preparation task to complete successfully before scheduling any other
     tasks of the job on the compute node. A Job Preparation task has completed
     successfully if it exits with exit code 0. If true and the Job Preparation
     task fails on a compute node, the Batch service retries the Job
     Preparation task up to its maximum retry count (as specified in the
     constraints element). If the task has still not completed successfully
     after all retries, then the Batch service will not schedule tasks of the
     job to the compute node. The compute node remains active and eligible to
     run tasks of other jobs. If false, the Batch service will not wait for the
     Job Preparation task to complete. In this case, other tasks of the job can
     start executing on the compute node while the Job Preparation task is
     still running; and even if the Job Preparation task fails, new tasks will
     continue to be scheduled on the node. The default value is true.
    :type wait_for_success: bool
    :param user_identity: The user identity under which the Job Preparation
     task runs. If omitted, the task runs as a non-administrative user unique
     to the task on Windows nodes, or a a non-administrative user unique to the
     pool on Linux nodes.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param rerun_on_node_reboot_after_success: Whether the Batch service
     should rerun the Job Preparation task after a compute node reboots. The
     Job Preparation task is always rerun if a compute node is reimaged, or if
     the Job Preparation task did not complete (e.g. because the reboot
     occurred while the task was running). Therefore, you should always write a
     Job Preparation task to be idempotent and to behave correctly if run
     multiple times. The default value is true.
    :type rerun_on_node_reboot_after_success: bool
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'wait_for_success': {'key': 'waitForSuccess', 'type': 'bool'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'rerun_on_node_reboot_after_success': {'key': 'rerunOnNodeRebootAfterSuccess', 'type': 'bool'},
    }

    def __init__(self, *, command_line: str, id: str=None, container_settings=None, resource_files=None,
                 environment_settings=None, constraints=None, wait_for_success: bool=None, user_identity=None,
                 rerun_on_node_reboot_after_success: bool=None, **kwargs) -> None:
        super(JobPreparationTask, self).__init__(**kwargs)
        self.id = id
        self.command_line = command_line
        self.container_settings = container_settings
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.constraints = constraints
        self.wait_for_success = wait_for_success
        self.user_identity = user_identity
        self.rerun_on_node_reboot_after_success = rerun_on_node_reboot_after_success


class JobReleaseTask(Model):
    """A Job Release task to run on job completion on any compute node where the
    job has run.

    The Job Release task runs when the job ends, because of one of the
    following: The user calls the Terminate Job API, or the Delete Job API
    while the job is still active, the job's maximum wall clock time constraint
    is reached, and the job is still active, or the job's Job Manager task
    completed, and the job is configured to terminate when the Job Manager
    completes. The Job Release task runs on each compute node where tasks of
    the job have run and the Job Preparation task ran and completed. If you
    reimage a compute node after it has run the Job Preparation task, and the
    job ends without any further tasks of the job running on that compute node
    (and hence the Job Preparation task does not re-run), then the Job Release
    task does not run on that node. If a compute node reboots while the Job
    Release task is still running, the Job Release task runs again when the
    compute node starts up. The job is not marked as complete until all Job
    Release tasks have completed. The Job Release task runs in the background.
    It does not occupy a scheduling slot; that is, it does not count towards
    the maxTasksPerNode limit specified on the pool.

    :param id: A string that uniquely identifies the Job Release task within
     the job. The ID can contain any combination of alphanumeric characters
     including hyphens and underscores and cannot contain more than 64
     characters. If you do not specify this property, the Batch service assigns
     a default value of 'jobrelease'. No other task in the job can have the
     same ID as the Job Release task. If you try to submit a task with the same
     ID, the Batch service rejects the request with error code
     TaskIdSameAsJobReleaseTask; if you are calling the REST API directly, the
     HTTP status code is 409 (Conflict).
    :type id: str
    :param command_line: The command line of the Job Release task. The command
     line does not run under a shell, and therefore cannot take advantage of
     shell features such as environment variable expansion. If you want to take
     advantage of such features, you should invoke the shell in the command
     line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c
     MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     Job Release task runs. When this is specified, all directories recursively
     below the AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch directories on
     the node) are mapped into the container, all task environment variables
     are mapped into the container, and the task command line is executed in
     the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. Files listed
     under this element are located in the task's working directory.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the Job Release task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param max_wall_clock_time: The maximum elapsed time that the Job Release
     task may run on a given compute node, measured from the time the task
     starts. If the task does not complete within the time limit, the Batch
     service terminates it. The default value is 15 minutes. You may not
     specify a timeout longer than 15 minutes. If you do, the Batch service
     rejects it with an error; if you are calling the REST API directly, the
     HTTP status code is 400 (Bad Request).
    :type max_wall_clock_time: timedelta
    :param retention_time: The minimum time to retain the task directory for
     the Job Release task on the compute node. After this time, the Batch
     service may delete the task directory and all its contents. The default is
     infinite, i.e. the task directory will be retained until the compute node
     is removed or reimaged.
    :type retention_time: timedelta
    :param user_identity: The user identity under which the Job Release task
     runs. If omitted, the task runs as a non-administrative user unique to the
     task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'max_wall_clock_time': {'key': 'maxWallClockTime', 'type': 'duration'},
        'retention_time': {'key': 'retentionTime', 'type': 'duration'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
    }

    def __init__(self, *, command_line: str, id: str=None, container_settings=None, resource_files=None,
                 environment_settings=None, max_wall_clock_time=None, retention_time=None, user_identity=None,
                 **kwargs) -> None:
        super(JobReleaseTask, self).__init__(**kwargs)
        self.id = id
        self.command_line = command_line
        self.container_settings = container_settings
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.max_wall_clock_time = max_wall_clock_time
        self.retention_time = retention_time
        self.user_identity = user_identity


class JobTemplate(Model):
    """A Job Template.

    :ivar type: The type of object described by the template. Must be:
     "Microsoft.Batch/batchAccounts/jobs"
    :type type: str
    :param api_version: The API version that the template conforms to.
    :type api_version: str
    :param properties: The specificaton of the job.
    :type properties: :class:`ExtendedJobParameter<azext.batch.models.ExtendedJobParameter>`
    """

    _validation = {
        'type': {'required': True, 'constant': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'id', 'type': 'str'},
        'api_version': {'key': 'apiVersion', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'ExtendedJobParameter'},
    }

    type = "Microsoft.Batch/batchAccounts/jobs"

    def __init__(self, *, properties, api_version: str=None, **kwargs) -> None:
        super(JobTemplate, self).__init__(**kwargs)
        self.properties = properties
        self.api_version = api_version


class MergeTask(Model):
    """An Azure Batch task template to repeat.

    :param str id: The ID of the merge task.
    :param display_name: A display name for the task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: The command line of the task. For multi-instance
     tasks, the command line is executed as the primary task, after the primary
     task and all subtasks have finished executing the coordination command
     line. The command line does not run under a shell, and therefore cannot
     take advantage of shell features such as environment variable expansion.
     If you want to take advantage of such features, you should invoke the
     shell in the command line, for example using "cmd /c MyCommand" in Windows
     or "/bin/sh -c MyCommand" in Linux.
    :type command_line: str
    :param exit_conditions: How the Batch service should respond when the task
     completes.
    :type exit_conditions: :class:`ExitConditions
     <azure.batch.models.ExitConditions>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. For
     multi-instance tasks, the resource files will only be downloaded to the
     compute node on which the primary task is executed.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param affinity_info: A locality hint that can be used by the Batch
     service to select a compute node on which to start the new task.
    :type affinity_info: :class:`AffinityInformation
     <azure.batch.models.AffinityInformation>`
    :param constraints: The execution constraints that apply to this task. If
     you do not specify constraints, the maxTaskRetryCount is the
     maxTaskRetryCount specified for the job, and the maxWallClockTime and
     retentionTime are infinite.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param user_identity: The user identity under which the task runs. If
     omitted, the task runs as a non-administrative user unique to the task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param depends_on: The tasks that this task depends on. This task will not
     be scheduled until all tasks that it depends on have completed
     successfully. If any of those tasks fail and exhaust their retry counts,
     this task will never be scheduled. If the job does not have
     usesTaskDependencies set to true, and this element is present, the request
     fails with error code TaskDependenciesNotSpecifiedOnJob.
    :type depends_on: :class:`TaskDependencies
     <azure.batch.models.TaskDependencies>`
    :param application_package_references: A list of application packages that
     the Batch service will deploy to the compute node before running the
     command line.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param authentication_token_settings: The settings for an authentication
     token that the task can use to perform Batch service operations. If this
     property is set, the Batch service provides the task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the task can carry out using the token depend on the settings. For
     example, a task can request job permissions in order to add other tasks to
     the job, or check the status of the job or of other tasks under the job.
    :type authentication_token_settings: :class:`AuthenticationTokenSettings
     <azure.batch.models.AuthenticationTokenSettings>`
    :param output_files: A list of output file references to up persisted once
     the task has completed.
    :type output_files: list of :class:`OutputFile
     <azext.batch.models.OutputFile>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'depends_on': {'key': 'dependsOn', 'type': 'TaskDependencies'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'},
    }

    def __init__(self, *, command_line: str, id: str=None, display_name: str=None, exit_conditions=None,
                 resource_files=None, environment_settings=None, affinity_info=None, constraints=None,
                 user_identity=None, depends_on=None, application_package_references=None,
                 authentication_token_settings=None, output_files=None, package_references=None, **kwargs) -> None:
        super(MergeTask, self).__init__(**kwargs)
        self.id = id
        self.display_name = display_name
        self.command_line = command_line
        self.exit_conditions = exit_conditions
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.affinity_info = affinity_info
        self.constraints = constraints
        self.user_identity = user_identity
        self.depends_on = depends_on
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
        self.output_files = output_files
        self.package_references = package_references


class MultiInstanceSettings(Model):
    """Settings which specify how to run a multi-instance task.

    Multi-instance tasks are commonly used to support MPI tasks.

    :param number_of_instances: The number of compute nodes required by the
     task. If omitted, the default is 1.
    :type number_of_instances: int
    :param coordination_command_line: The command line to run on all the
     compute nodes to enable them to coordinate when the primary runs the main
     task command. A typical coordination command line launches a background
     service and verifies that the service is ready to process inter-node
     messages.
    :type coordination_command_line: str
    :param common_resource_files: A list of files that the Batch service will
     download before running the coordination command line. The difference
     between common resource files and task resource files is that common
     resource files are downloaded for all subtasks including the primary,
     whereas task resource files are downloaded only for the primary. Also note
     that these resource files are not downloaded to the task working
     directory, but instead are downloaded to the task root directory (one
     directory above the working directory).
    :type common_resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    """

    _validation = {
        'coordination_command_line': {'required': True},
    }

    _attribute_map = {
        'number_of_instances': {'key': 'numberOfInstances', 'type': 'int'},
        'coordination_command_line': {'key': 'coordinationCommandLine', 'type': 'str'},
        'common_resource_files': {'key': 'commonResourceFiles', 'type': '[ExtendedResourceFile]'},
    }

    def __init__(self, *, coordination_command_line: int, number_of_instances: str=None,
                 common_resource_files=None, **kwargs) -> None:
        super(MultiInstanceSettings, self).__init__(**kwargs)
        self.number_of_instances = number_of_instances
        self.coordination_command_line = coordination_command_line
        self.common_resource_files = common_resource_files


class OutputFileAutoStorageDestination(Model):
    """An speficition of output files upload destination that uses an
    auto-storage file group.

    :param str file_group: The name of the file group that the output files will
     be uploaded to.
    :param str path: The destination path within the file group that the files will
     be uploaded to. Is the output file specification refers to a single file, this will
     be treated as a file name. If the output file specification refers to potentially
     multiple files, this will be treated as a subfolder.
    """

    _validation = {
        'file_group': {'required': True}
    }

    _attribute_map = {
        'file_group': {'key': 'fileGroup', 'type': 'str'},
        'path': {'key': 'path', 'type': 'str'},
    }

    def __init__(self, *, file_group: str, path: str=None, **kwargs) -> None:
        super(OutputFileAutoStorageDestination, self).__init__(**kwargs)
        self.file_group = file_group
        self.path = path


class OutputFile(Model):
    """A specification for uploading files from an Azure Batch node to another
    location after the Batch service has finished executing the task process.

    :param file_pattern: A pattern indicating which file(s) to upload. Both
     relative and absolute paths are supported. Relative paths are relative to
     the task working directory. The following wildcards are supported: *
     matches 0 or more characters (for example pattern abc* would match abc or
     abcdef), ** matches any directory, ? matches any single character, [abc]
     matches one character in the brackets, and [a-c] matches one character in
     the range. Brackets can include a negation to match any character not
     specified (for example [!abc] matches any character but a, b, or c). If a
     file name starts with "." it is ignored by default but may be matched by
     specifying it explicitly (for example *.gif will not match .a.gif, but
     .*.gif will). A simple example: **\\*.txt matches any file that does not
     start in '.' and ends with .txt in the task working directory or any
     subdirectory. If the filename contains a wildcard character it can be
     escaped using brackets (for example abc[*] would match a file named abc*).
     Note that both \\ and / are treated as directory separators on Windows,
     but only / is on Linux. Environment variables (%var% on Windows or $var on
     Linux) are expanded prior to the pattern being applied.
    :type file_pattern: str
    :param destination: The destination for the output file(s).
    :type destination: :class:`ExtendedOutputFileDestination
     <azext.batch.models.ExtendedOutputFileDestination>`
    :param upload_options: Additional options for the upload operation,
     including under what conditions to perform the upload.
    :type upload_options: :class:`OutputFileUploadOptions
     <azure.batch.models.OutputFileUploadOptions>`
    """

    _validation = {
        'file_pattern': {'required': True},
        'destination': {'required': True},
        'upload_options': {'required': True},
    }

    _attribute_map = {
        'file_pattern': {'key': 'filePattern', 'type': 'str'},
        'destination': {'key': 'destination', 'type': 'ExtendedOutputFileDestination'},
        'upload_options': {'key': 'uploadOptions', 'type': 'OutputFileUploadOptions'},
    }

    def __init__(self, *, file_pattern: str, destination, upload_options, **kwargs) -> None:
        super(OutputFile, self).__init__(**kwargs)
        self.file_pattern = file_pattern
        self.destination = destination
        self.upload_options = upload_options


class ParameterSet(Model):
    """A set of parametric sweep range range parameters.

    :param int start: The starting value of the sweep.
    :param int end: The ending value of the sweep (inclusive).
    :param int step: The incremental step value, default is 1. The step value
     can be negative (i.e. a decending sweep), but only id the start value is
     a higher value than the end.
    """

    _validation = {
        'start': {'required': True},
        'end': {'required': True},
    }

    _attribute_map = {
        'start': {'key': 'start', 'type': 'int'},
        'end': {'key': 'end', 'type': 'int'},
        'step': {'key': 'step', 'type': 'int'},
    }

    def __init__(self, *, start: int, end: int, step: int=1, **kwargs) -> None:
        super(ParameterSet, self).__init__(**kwargs)
        try:
            self.start = int(start)
            self.end = int(end)
            self.step = int(step)
        except (TypeError, ValueError):
            raise ValueError("'start', 'end' and 'step' parameters must be integers.")
        if step == 0:
            raise ValueError("'step' parameter cannot be 0.")
        elif start > end and step > 0:
            raise ValueError(
                "'step' must be a negative number when 'start' is greater than 'end'")
        elif start < end and step < 0:
            raise ValueError(
                "'step' must be a positive number when 'end' is greater than 'start'")


class ParametricSweepTaskFactory(TaskFactoryBase):
    class PoolTemplate(Model):
        """A Pool Template.

        :ivar type: The type of object described by the template. Must be:
         "Microsoft.Batch/batchAccounts/pools"
        :type type: str
        :param api_version: The API version that the template conforms to.
        :type api_version: str
        :param properties: The specificaton of the pool.
        :type properties: :class:`ExtendedPoolParameter<azext.batch.models.ExtendedPoolParameter>`
        """

        _validation = {
            'type': {'required': True, 'constant': True},
            'properties': {'required': True},
        }

        _attribute_map = {
            'type': {'key': 'id', 'type': 'str'},
            'api_version': {'key': 'apiVersion', 'type': 'str'},
            'properties': {'key': 'properties',
                           'type': 'ExtendedPoolParameter'},
        }

        type = "Microsoft.Batch/batchAccounts/pools"

        def __init__(self, *, properties: str, api_version=None,
                     **kwargs) -> None:
            super(PoolTemplate, self).__init__(**kwargs)
            self.properties = properties
            self.api_version = api_version


class PoolTemplate(Model):
    """A Pool Template.

    :ivar type: The type of object described by the template. Must be:
     "Microsoft.Batch/batchAccounts/pools"
    :type type: str
    :param api_version: The API version that the template conforms to.
    :type api_version: str
    :param properties: The specificaton of the pool.
    :type properties: :class:`ExtendedPoolParameter<azext.batch.models.ExtendedPoolParameter>`
    """

    _validation = {
        'type': {'required': True, 'constant': True},
        'properties': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'id', 'type': 'str'},
        'api_version': {'key': 'apiVersion', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'ExtendedPoolParameter'},
    }

    type = "Microsoft.Batch/batchAccounts/pools"

    def __init__(self, *, properties: str, api_version=None, **kwargs) -> None:
        super(PoolTemplate, self).__init__(**kwargs)
        self.properties = properties
        self.api_version = api_version


class RepeatTask(Model):
    """An Azure Batch task template to repeat.

    :param display_name: A display name for the task. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param command_line: The command line of the task.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     task runs. If the pool that will run this task has containerConfiguration
     set, this must be set as well. If the pool that will run this task doesn't
     have containerConfiguration set, this must not be set. When this is
     specified, all directories recursively below the AZ_BATCH_NODE_ROOT_DIR
     (the root of Azure Batch directories on the node) are mapped into the
     container, all task environment variables are mapped into the container,
     and the task command line is executed in the container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param exit_conditions: How the Batch service should respond when the task
     completes.
    :type exit_conditions: :class:`ExitConditions
     <azure.batch.models.ExitConditions>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param affinity_info: A locality hint that can be used by the Batch
     service to select a compute node on which to start the new task.
    :type affinity_info: :class:`AffinityInformation
     <azure.batch.models.AffinityInformation>`
    :param constraints: The execution constraints that apply to this task. If
     you do not specify constraints, the maxTaskRetryCount is the
     maxTaskRetryCount specified for the job, and the maxWallClockTime and
     retentionTime are infinite.
    :type constraints: :class:`TaskConstraints
     <azure.batch.models.TaskConstraints>`
    :param user_identity: The user identity under which the task runs. If
     omitted, the task runs as a non-administrative user unique to the task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param application_package_references: A list of application packages that
     the Batch service will deploy to the compute node before running the
     command line.
    :type application_package_references: list of
     :class:`ApplicationPackageReference
     <azure.batch.models.ApplicationPackageReference>`
    :param authentication_token_settings: The settings for an authentication
     token that the task can use to perform Batch service operations. If this
     property is set, the Batch service provides the task with an
     authentication token which can be used to authenticate Batch service
     operations without requiring an account access key. The token is provided
     via the AZ_BATCH_AUTHENTICATION_TOKEN environment variable. The operations
     that the task can carry out using the token depend on the settings. For
     example, a task can request job permissions in order to add other tasks to
     the job, or check the status of the job or of other tasks under the job.
    :type authentication_token_settings: :class:`AuthenticationTokenSettings
     <azure.batch.models.AuthenticationTokenSettings>`
    :param output_files: A list of output file references to up persisted once
     the task has completed.
    :type output_files: list of :class:`OutputFile
     <azext.batch.models.OutputFile>`
    :param package_references: A list of packages to be installed on the compute
     nodes. Must be of a Package Manager type in accordance with the selected
     operating system.
    :type package_references: list of :class:`PackageReferenceBase
     <azext.batch.models.PackageReferenceBase>`
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'display_name': {'key': 'displayName', 'type': 'str'},
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'exit_conditions': {'key': 'exitConditions', 'type': 'ExitConditions'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'affinity_info': {'key': 'affinityInfo', 'type': 'AffinityInformation'},
        'constraints': {'key': 'constraints', 'type': 'TaskConstraints'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'application_package_references': {'key': 'applicationPackageReferences',
                                           'type': '[ApplicationPackageReference]'},
        'authentication_token_settings': {'key': 'authenticationTokenSettings',
                                          'type': 'AuthenticationTokenSettings'},
        'output_files': {'key': 'outputFiles', 'type': '[OutputFile]'},
        'package_references': {'key': 'packageReferences', 'type': '[PackageReferenceBase]'}
    }

    def __init__(self, *, command_line: str, display_name: str=None, container_settings=None, exit_conditions=None,
                 resource_files=None, environment_settings=None, affinity_info=None, constraints=None,
                 user_identity=None, application_package_references=None, authentication_token_settings=None,
                 output_files=None, package_references=None, **kwargs) -> None:
        super(RepeatTask, self).__init__(**kwargs)
        self.display_name = display_name
        self.command_line = command_line
        self.container_settings = container_settings
        self.exit_conditions = exit_conditions
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.affinity_info = affinity_info
        self.constraints = constraints
        self.user_identity = user_identity
        self.application_package_references = application_package_references
        self.authentication_token_settings = authentication_token_settings
        self.output_files = output_files
        self.package_references = package_references


class StartTask(Model):
    """A task which is run when a compute node joins a pool in the Azure Batch
    service, or when the compute node is rebooted or reimaged.

    :param command_line: The command line of the start task. The command line
     does not run under a shell, and therefore cannot take advantage of shell
     features such as environment variable expansion. If you want to take
     advantage of such features, you should invoke the shell in the command
     line, for example using "cmd /c MyCommand" in Windows or "/bin/sh -c
     MyCommand" in Linux.
    :type command_line: str
    :param container_settings: The settings for the container under which the
     start task runs. When this is specified, all directories recursively below
     the AZ_BATCH_NODE_ROOT_DIR (the root of Azure Batch directories on the
     node) are mapped into the container, all task environment variables are
     mapped into the container, and the task command line is executed in the
     container.
    :type container_settings: :class:`TaskContainerSettings
     <azure.batch.models.TaskContainerSettings>`
    :param resource_files: A list of files that the Batch service will
     download to the compute node before running the command line. Files listed
     under this element are located in the task's working directory.
    :type resource_files: list of :class:`ExtendedResourceFile
     <azext.batch.models.ExtendedResourceFile>`
    :param environment_settings: A list of environment variable settings for
     the start task.
    :type environment_settings: list of :class:`EnvironmentSetting
     <azure.batch.models.EnvironmentSetting>`
    :param user_identity: The user identity under which the start task runs.
     If omitted, the task runs as a non-administrative user unique to the task.
    :type user_identity: :class:`UserIdentity
     <azure.batch.models.UserIdentity>`
    :param max_task_retry_count: The maximum number of times the task may be
     retried. The Batch service retries a task if its exit code is nonzero.
     Note that this value specifically controls the number of retries. The
     Batch service will try the task once, and may then retry up to this limit.
     For example, if the maximum retry count is 3, Batch tries the task up to 4
     times (one initial try and 3 retries). If the maximum retry count is 0,
     the Batch service does not retry the task. If the maximum retry count is
     -1, the Batch service retries the task without limit.
    :type max_task_retry_count: int
    :param wait_for_success: Whether the Batch service should wait for the
     start task to complete successfully (that is, to exit with exit code 0)
     before scheduling any tasks on the compute node. If true and the start
     task fails on a compute node, the Batch service retries the start task up
     to its maximum retry count (maxTaskRetryCount). If the task has still not
     completed successfully after all retries, then the Batch service marks the
     compute node unusable, and will not schedule tasks to it. This condition
     can be detected via the node state and failure info details. If false, the
     Batch service will not wait for the start task to complete. In this case,
     other tasks can start executing on the compute node while the start task
     is still running; and even if the start task fails, new tasks will
     continue to be scheduled on the node. The default is false.
    :type wait_for_success: bool
    """

    _validation = {
        'command_line': {'required': True},
    }

    _attribute_map = {
        'command_line': {'key': 'commandLine', 'type': 'str'},
        'container_settings': {'key': 'containerSettings', 'type': 'TaskContainerSettings'},
        'resource_files': {'key': 'resourceFiles', 'type': '[ExtendedResourceFile]'},
        'environment_settings': {'key': 'environmentSettings', 'type': '[EnvironmentSetting]'},
        'user_identity': {'key': 'userIdentity', 'type': 'UserIdentity'},
        'max_task_retry_count': {'key': 'maxTaskRetryCount', 'type': 'int'},
        'wait_for_success': {'key': 'waitForSuccess', 'type': 'bool'},
    }

    def __init__(self, *, command_line: str, container_settings=None, resource_files=None, environment_settings=None,
                 user_identity=None, max_task_retry_count: int=None, wait_for_success: bool=None, **kwargs) -> None:
        super(StartTask, self).__init__(**kwargs)
        self.command_line = command_line
        self.container_settings = container_settings
        self.resource_files = resource_files
        self.environment_settings = environment_settings
        self.user_identity = user_identity
        self.max_task_retry_count = max_task_retry_count
        self.wait_for_success = wait_for_success


class TaskCollectionTaskFactory(TaskFactoryBase):
    """A Task Factory for adding a predefined collection of tasks automatically
    to a job on submission.

    :param tasks: A list if task parameters, each of which will be added straight to the job.
    :type tasks: A list of :class:`ExtendedTaskParameter
     <azext.batch.models.ExtendedTaskParameter>`
    """

    _validation = {
        'type': {'required': True},
        'tasks': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'tasks': {'key': 'tasks', 'type': '[ExtendedTaskParameter]'},
    }

    def __init__(self, *, tasks, **kwargs) -> None:
        super(TaskCollectionTaskFactory, self).__init__(**kwargs)
        self.tasks = tasks
        self.type = 'taskCollection'


class YumPackageReference(PackageReferenceBase):
    """A reference to a package to be installed using the YUM package
    manager on a Linux node.

    :param str id: The name of the package.
    :param str version: The version of the package to be installed. If omitted,
     the latest version (according to the package repository) will be installed.
    :param bool disable_excludes: Whether to allow packages that might otherwise
     be excluded by VM configuration (e.g. kernel packages). Default is False.
    """

    _validation = {
        'type': {'required': True},
        'id': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'disable_excludes': {'key': 'disableExcludes', 'type': 'bool'}
    }

    def __init__(self, *, id: str, version: str=None, disable_excludes: bool=None, **kwargs) -> None:
        super(YumPackageReference, self).__init__(id=id, version=version, **kwargs)
        self.disable_excludes = disable_excludes
        self.type = 'yumPackage'
