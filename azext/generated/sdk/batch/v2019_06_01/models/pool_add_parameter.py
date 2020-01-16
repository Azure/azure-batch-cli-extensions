# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PoolAddParameter(Model):
    """A Pool in the Azure Batch service to add.

    All required parameters must be populated in order to send to Azure.

    :param id: Required. A string that uniquely identifies the Pool within the
     Account. The ID can contain any combination of alphanumeric characters
     including hyphens and underscores, and cannot contain more than 64
     characters. The ID is case-preserving and case-insensitive (that is, you
     may not have two Pool IDs within an Account that differ only by case).
    :type id: str
    :param display_name: The display name for the Pool. The display name need
     not be unique and can contain any Unicode characters up to a maximum
     length of 1024.
    :type display_name: str
    :param vm_size: Required. The size of virtual machines in the Pool. All
     virtual machines in a Pool are the same size. For information about
     available sizes of virtual machines for Cloud Services Pools (pools
     created with cloudServiceConfiguration), see Sizes for Cloud Services
     (https://azure.microsoft.com/documentation/articles/cloud-services-sizes-specs/).
     Batch supports all Cloud Services VM sizes except ExtraSmall, A1V2 and
     A2V2. For information about available VM sizes for Pools using Images from
     the Virtual Machines Marketplace (pools created with
     virtualMachineConfiguration) see Sizes for Virtual Machines (Linux)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-linux-sizes/)
     or Sizes for Virtual Machines (Windows)
     (https://azure.microsoft.com/documentation/articles/virtual-machines-windows-sizes/).
     Batch supports all Azure VM sizes except STANDARD_A0 and those with
     premium storage (STANDARD_GS, STANDARD_DS, and STANDARD_DSV2 series).
    :type vm_size: str
    :param cloud_service_configuration: The cloud service configuration for
     the Pool. This property and virtualMachineConfiguration are mutually
     exclusive and one of the properties must be specified. This property
     cannot be specified if the Batch Account was created with its
     poolAllocationMode property set to 'UserSubscription'.
    :type cloud_service_configuration:
     ~azure.batch.models.CloudServiceConfiguration
    :param virtual_machine_configuration: The virtual machine configuration
     for the Pool. This property and cloudServiceConfiguration are mutually
     exclusive and one of the properties must be specified.
    :type virtual_machine_configuration:
     ~azure.batch.models.VirtualMachineConfiguration
    :param resize_timeout: The timeout for allocation of Compute Nodes to the
     Pool. This timeout applies only to manual scaling; it has no effect when
     enableAutoScale is set to true. The default value is 15 minutes. The
     minimum value is 5 minutes. If you specify a value less than 5 minutes,
     the Batch service returns an error; if you are calling the REST API
     directly, the HTTP status code is 400 (Bad Request).
    :type resize_timeout: timedelta
    :param target_dedicated_nodes: The desired number of dedicated Compute
     Nodes in the Pool. This property must not be specified if enableAutoScale
     is set to true. If enableAutoScale is set to false, then you must set
     either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_dedicated_nodes: int
    :param target_low_priority_nodes: The desired number of low-priority
     Compute Nodes in the Pool. This property must not be specified if
     enableAutoScale is set to true. If enableAutoScale is set to false, then
     you must set either targetDedicatedNodes, targetLowPriorityNodes, or both.
    :type target_low_priority_nodes: int
    :param enable_auto_scale: Whether the Pool size should automatically
     adjust over time. If false, at least one of targetDedicateNodes and
     targetLowPriorityNodes must be specified. If true, the autoScaleFormula
     property is required and the Pool automatically resizes according to the
     formula. The default value is false.
    :type enable_auto_scale: bool
    :param auto_scale_formula: A formula for the desired number of Compute
     Nodes in the Pool. This property must not be specified if enableAutoScale
     is set to false. It is required if enableAutoScale is set to true. The
     formula is checked for validity before the Pool is created. If the formula
     is not valid, the Batch service rejects the request with detailed error
     information. For more information about specifying this formula, see
     'Automatically scale Compute Nodes in an Azure Batch Pool'
     (https://azure.microsoft.com/documentation/articles/batch-automatic-scaling/).
    :type auto_scale_formula: str
    :param auto_scale_evaluation_interval: The time interval at which to
     automatically adjust the Pool size according to the autoscale formula. The
     default value is 15 minutes. The minimum and maximum value are 5 minutes
     and 168 hours respectively. If you specify a value less than 5 minutes or
     greater than 168 hours, the Batch service returns an error; if you are
     calling the REST API directly, the HTTP status code is 400 (Bad Request).
    :type auto_scale_evaluation_interval: timedelta
    :param enable_inter_node_communication: Whether the Pool permits direct
     communication between Compute Nodes. Enabling inter-node communication
     limits the maximum size of the Pool due to deployment restrictions on the
     Compute Nodes of the Pool. This may result in the Pool not reaching its
     desired size. The default value is false.
    :type enable_inter_node_communication: bool
    :param network_configuration: The network configuration for the Pool.
    :type network_configuration: ~azure.batch.models.NetworkConfiguration
    :param start_task: A Task specified to run on each Compute Node as it
     joins the Pool. The Task runs when the Compute Node is added to the Pool
     or when the Compute Node is restarted.
    :type start_task: ~azure.batch.models.StartTask
    :param certificate_references: The list of Certificates to be installed on
     each Compute Node in the Pool. For Windows Nodes, the Batch service
     installs the Certificates to the specified Certificate store and location.
     For Linux Compute Nodes, the Certificates are stored in a directory inside
     the Task working directory and an environment variable
     AZ_BATCH_CERTIFICATES_DIR is supplied to the Task to query for this
     location. For Certificates with visibility of 'remoteUser', a 'certs'
     directory is created in the user's home directory (e.g.,
     /home/{user-name}/certs) and Certificates are placed in that directory.
    :type certificate_references:
     list[~azure.batch.models.CertificateReference]
    :param application_package_references: The list of Packages to be
     installed on each Compute Node in the Pool. Changes to Package references
     affect all new Nodes joining the Pool, but do not affect Compute Nodes
     that are already in the Pool until they are rebooted or reimaged. There is
     a maximum of 10 Package references on any given Pool.
    :type application_package_references:
     list[~azure.batch.models.ApplicationPackageReference]
    :param application_licenses: The list of application licenses the Batch
     service will make available on each Compute Node in the Pool. The list of
     application licenses must be a subset of available Batch service
     application licenses. If a license is requested which is not supported,
     Pool creation will fail.
    :type application_licenses: list[str]
    :param max_tasks_per_node: The maximum number of Tasks that can run
     concurrently on a single Compute Node in the Pool. The default value is 1.
     The maximum value is the smaller of 4 times the number of cores of the
     vmSize of the Pool or 256.
    :type max_tasks_per_node: int
    :param task_scheduling_policy: How Tasks are distributed across Compute
     Nodes in a Pool. If not specified, the default is spread.
    :type task_scheduling_policy: ~azure.batch.models.TaskSchedulingPolicy
    :param user_accounts: The list of user Accounts to be created on each
     Compute Node in the Pool.
    :type user_accounts: list[~azure.batch.models.UserAccount]
    :param metadata: A list of name-value pairs associated with the Pool as
     metadata. The Batch service does not assign any meaning to metadata; it is
     solely for the use of user code.
    :type metadata: list[~azure.batch.models.MetadataItem]
    """

    _validation = {
        'id': {'required': True},
        'vm_size': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'vm_size': {'key': 'vmSize', 'type': 'str'},
        'cloud_service_configuration': {'key': 'cloudServiceConfiguration', 'type': 'CloudServiceConfiguration'},
        'virtual_machine_configuration': {'key': 'virtualMachineConfiguration', 'type': 'VirtualMachineConfiguration'},
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
        'application_package_references': {'key': 'applicationPackageReferences', 'type': '[ApplicationPackageReference]'},
        'application_licenses': {'key': 'applicationLicenses', 'type': '[str]'},
        'max_tasks_per_node': {'key': 'maxTasksPerNode', 'type': 'int'},
        'task_scheduling_policy': {'key': 'taskSchedulingPolicy', 'type': 'TaskSchedulingPolicy'},
        'user_accounts': {'key': 'userAccounts', 'type': '[UserAccount]'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
    }

    def __init__(self, **kwargs):
        super(PoolAddParameter, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.display_name = kwargs.get('display_name', None)
        self.vm_size = kwargs.get('vm_size', None)
        self.cloud_service_configuration = kwargs.get('cloud_service_configuration', None)
        self.virtual_machine_configuration = kwargs.get('virtual_machine_configuration', None)
        self.resize_timeout = kwargs.get('resize_timeout', None)
        self.target_dedicated_nodes = kwargs.get('target_dedicated_nodes', None)
        self.target_low_priority_nodes = kwargs.get('target_low_priority_nodes', None)
        self.enable_auto_scale = kwargs.get('enable_auto_scale', None)
        self.auto_scale_formula = kwargs.get('auto_scale_formula', None)
        self.auto_scale_evaluation_interval = kwargs.get('auto_scale_evaluation_interval', None)
        self.enable_inter_node_communication = kwargs.get('enable_inter_node_communication', None)
        self.network_configuration = kwargs.get('network_configuration', None)
        self.start_task = kwargs.get('start_task', None)
        self.certificate_references = kwargs.get('certificate_references', None)
        self.application_package_references = kwargs.get('application_package_references', None)
        self.application_licenses = kwargs.get('application_licenses', None)
        self.max_tasks_per_node = kwargs.get('max_tasks_per_node', None)
        self.task_scheduling_policy = kwargs.get('task_scheduling_policy', None)
        self.user_accounts = kwargs.get('user_accounts', None)
        self.metadata = kwargs.get('metadata', None)
