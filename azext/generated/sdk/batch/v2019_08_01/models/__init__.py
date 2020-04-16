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

try:
    from .pool_usage_metrics_py3 import PoolUsageMetrics
    from .image_reference_py3 import ImageReference
    from .image_information_py3 import ImageInformation
    from .authentication_token_settings_py3 import AuthenticationTokenSettings
    from .usage_statistics_py3 import UsageStatistics
    from .resource_statistics_py3 import ResourceStatistics
    from .pool_statistics_py3 import PoolStatistics
    from .job_statistics_py3 import JobStatistics
    from .name_value_pair_py3 import NameValuePair
    from .delete_certificate_error_py3 import DeleteCertificateError
    from .certificate_py3 import Certificate
    from .application_package_reference_py3 import ApplicationPackageReference
    from .application_summary_py3 import ApplicationSummary
    from .certificate_add_parameter_py3 import CertificateAddParameter
    from .file_properties_py3 import FileProperties
    from .node_file_py3 import NodeFile
    from .schedule_py3 import Schedule
    from .job_constraints_py3 import JobConstraints
    from .job_network_configuration_py3 import JobNetworkConfiguration
    from .container_registry_py3 import ContainerRegistry
    from .task_container_settings_py3 import TaskContainerSettings
    from .resource_file_py3 import ResourceFile
    from .environment_setting_py3 import EnvironmentSetting
    from .exit_options_py3 import ExitOptions
    from .exit_code_mapping_py3 import ExitCodeMapping
    from .exit_code_range_mapping_py3 import ExitCodeRangeMapping
    from .exit_conditions_py3 import ExitConditions
    from .auto_user_specification_py3 import AutoUserSpecification
    from .user_identity_py3 import UserIdentity
    from .linux_user_configuration_py3 import LinuxUserConfiguration
    from .windows_user_configuration_py3 import WindowsUserConfiguration
    from .user_account_py3 import UserAccount
    from .task_constraints_py3 import TaskConstraints
    from .output_file_blob_container_destination_py3 import OutputFileBlobContainerDestination
    from .output_file_destination_py3 import OutputFileDestination
    from .output_file_upload_options_py3 import OutputFileUploadOptions
    from .output_file_py3 import OutputFile
    from .job_manager_task_py3 import JobManagerTask
    from .job_preparation_task_py3 import JobPreparationTask
    from .job_release_task_py3 import JobReleaseTask
    from .task_scheduling_policy_py3 import TaskSchedulingPolicy
    from .start_task_py3 import StartTask
    from .certificate_reference_py3 import CertificateReference
    from .metadata_item_py3 import MetadataItem
    from .cloud_service_configuration_py3 import CloudServiceConfiguration
    from .windows_configuration_py3 import WindowsConfiguration
    from .data_disk_py3 import DataDisk
    from .container_configuration_py3 import ContainerConfiguration
    from .virtual_machine_configuration_py3 import VirtualMachineConfiguration
    from .network_security_group_rule_py3 import NetworkSecurityGroupRule
    from .inbound_nat_pool_py3 import InboundNATPool
    from .pool_endpoint_configuration_py3 import PoolEndpointConfiguration
    from .network_configuration_py3 import NetworkConfiguration
    from .azure_blob_file_system_configuration_py3 import AzureBlobFileSystemConfiguration
    from .nfs_mount_configuration_py3 import NFSMountConfiguration
    from .cifs_mount_configuration_py3 import CIFSMountConfiguration
    from .azure_file_share_configuration_py3 import AzureFileShareConfiguration
    from .mount_configuration_py3 import MountConfiguration
    from .pool_specification_py3 import PoolSpecification
    from .auto_pool_specification_py3 import AutoPoolSpecification
    from .pool_information_py3 import PoolInformation
    from .job_specification_py3 import JobSpecification
    from .recent_job_py3 import RecentJob
    from .job_schedule_execution_information_py3 import JobScheduleExecutionInformation
    from .job_schedule_statistics_py3 import JobScheduleStatistics
    from .cloud_job_schedule_py3 import CloudJobSchedule
    from .job_schedule_add_parameter_py3 import JobScheduleAddParameter
    from .job_scheduling_error_py3 import JobSchedulingError
    from .job_execution_information_py3 import JobExecutionInformation
    from .cloud_job_py3 import CloudJob
    from .job_add_parameter_py3 import JobAddParameter
    from .task_container_execution_information_py3 import TaskContainerExecutionInformation
    from .task_failure_information_py3 import TaskFailureInformation
    from .job_preparation_task_execution_information_py3 import JobPreparationTaskExecutionInformation
    from .job_release_task_execution_information_py3 import JobReleaseTaskExecutionInformation
    from .job_preparation_and_release_task_execution_information_py3 import JobPreparationAndReleaseTaskExecutionInformation
    from .task_counts_py3 import TaskCounts
    from .auto_scale_run_error_py3 import AutoScaleRunError
    from .auto_scale_run_py3 import AutoScaleRun
    from .resize_error_py3 import ResizeError
    from .cloud_pool_py3 import CloudPool
    from .pool_add_parameter_py3 import PoolAddParameter
    from .affinity_information_py3 import AffinityInformation
    from .task_execution_information_py3 import TaskExecutionInformation
    from .compute_node_information_py3 import ComputeNodeInformation
    from .node_agent_information_py3 import NodeAgentInformation
    from .multi_instance_settings_py3 import MultiInstanceSettings
    from .task_statistics_py3 import TaskStatistics
    from .task_id_range_py3 import TaskIdRange
    from .task_dependencies_py3 import TaskDependencies
    from .cloud_task_py3 import CloudTask
    from .task_add_parameter_py3 import TaskAddParameter
    from .task_add_collection_parameter_py3 import TaskAddCollectionParameter
    from .error_message_py3 import ErrorMessage
    from .batch_error_detail_py3 import BatchErrorDetail
    from .batch_error_py3 import BatchError, BatchErrorException
    from .task_add_result_py3 import TaskAddResult
    from .task_add_collection_result_py3 import TaskAddCollectionResult
    from .subtask_information_py3 import SubtaskInformation
    from .cloud_task_list_subtasks_result_py3 import CloudTaskListSubtasksResult
    from .task_information_py3 import TaskInformation
    from .start_task_information_py3 import StartTaskInformation
    from .compute_node_error_py3 import ComputeNodeError
    from .inbound_endpoint_py3 import InboundEndpoint
    from .compute_node_endpoint_configuration_py3 import ComputeNodeEndpointConfiguration
    from .compute_node_py3 import ComputeNode
    from .compute_node_user_py3 import ComputeNodeUser
    from .compute_node_get_remote_login_settings_result_py3 import ComputeNodeGetRemoteLoginSettingsResult
    from .job_schedule_patch_parameter_py3 import JobSchedulePatchParameter
    from .job_schedule_update_parameter_py3 import JobScheduleUpdateParameter
    from .job_disable_parameter_py3 import JobDisableParameter
    from .job_terminate_parameter_py3 import JobTerminateParameter
    from .job_patch_parameter_py3 import JobPatchParameter
    from .job_update_parameter_py3 import JobUpdateParameter
    from .pool_enable_auto_scale_parameter_py3 import PoolEnableAutoScaleParameter
    from .pool_evaluate_auto_scale_parameter_py3 import PoolEvaluateAutoScaleParameter
    from .pool_resize_parameter_py3 import PoolResizeParameter
    from .pool_update_properties_parameter_py3 import PoolUpdatePropertiesParameter
    from .pool_patch_parameter_py3 import PoolPatchParameter
    from .task_update_parameter_py3 import TaskUpdateParameter
    from .node_update_user_parameter_py3 import NodeUpdateUserParameter
    from .node_reboot_parameter_py3 import NodeRebootParameter
    from .node_reimage_parameter_py3 import NodeReimageParameter
    from .node_disable_scheduling_parameter_py3 import NodeDisableSchedulingParameter
    from .node_remove_parameter_py3 import NodeRemoveParameter
    from .upload_batch_service_logs_configuration_py3 import UploadBatchServiceLogsConfiguration
    from .upload_batch_service_logs_result_py3 import UploadBatchServiceLogsResult
    from .node_counts_py3 import NodeCounts
    from .pool_node_counts_py3 import PoolNodeCounts
    from .application_list_options_py3 import ApplicationListOptions
    from .application_get_options_py3 import ApplicationGetOptions
    from .pool_list_usage_metrics_options_py3 import PoolListUsageMetricsOptions
    from .pool_get_all_lifetime_statistics_options_py3 import PoolGetAllLifetimeStatisticsOptions
    from .pool_add_options_py3 import PoolAddOptions
    from .pool_list_options_py3 import PoolListOptions
    from .pool_delete_options_py3 import PoolDeleteOptions
    from .pool_exists_options_py3 import PoolExistsOptions
    from .pool_get_options_py3 import PoolGetOptions
    from .pool_patch_options_py3 import PoolPatchOptions
    from .pool_disable_auto_scale_options_py3 import PoolDisableAutoScaleOptions
    from .pool_enable_auto_scale_options_py3 import PoolEnableAutoScaleOptions
    from .pool_evaluate_auto_scale_options_py3 import PoolEvaluateAutoScaleOptions
    from .pool_resize_options_py3 import PoolResizeOptions
    from .pool_stop_resize_options_py3 import PoolStopResizeOptions
    from .pool_update_properties_options_py3 import PoolUpdatePropertiesOptions
    from .pool_remove_nodes_options_py3 import PoolRemoveNodesOptions
    from .account_list_supported_images_options_py3 import AccountListSupportedImagesOptions
    from .account_list_pool_node_counts_options_py3 import AccountListPoolNodeCountsOptions
    from .job_get_all_lifetime_statistics_options_py3 import JobGetAllLifetimeStatisticsOptions
    from .job_delete_options_py3 import JobDeleteOptions
    from .job_get_options_py3 import JobGetOptions
    from .job_patch_options_py3 import JobPatchOptions
    from .job_update_options_py3 import JobUpdateOptions
    from .job_disable_options_py3 import JobDisableOptions
    from .job_enable_options_py3 import JobEnableOptions
    from .job_terminate_options_py3 import JobTerminateOptions
    from .job_add_options_py3 import JobAddOptions
    from .job_list_options_py3 import JobListOptions
    from .job_list_from_job_schedule_options_py3 import JobListFromJobScheduleOptions
    from .job_list_preparation_and_release_task_status_options_py3 import JobListPreparationAndReleaseTaskStatusOptions
    from .job_get_task_counts_options_py3 import JobGetTaskCountsOptions
    from .certificate_add_options_py3 import CertificateAddOptions
    from .certificate_list_options_py3 import CertificateListOptions
    from .certificate_cancel_deletion_options_py3 import CertificateCancelDeletionOptions
    from .certificate_delete_options_py3 import CertificateDeleteOptions
    from .certificate_get_options_py3 import CertificateGetOptions
    from .file_delete_from_task_options_py3 import FileDeleteFromTaskOptions
    from .file_get_from_task_options_py3 import FileGetFromTaskOptions
    from .file_get_properties_from_task_options_py3 import FileGetPropertiesFromTaskOptions
    from .file_delete_from_compute_node_options_py3 import FileDeleteFromComputeNodeOptions
    from .file_get_from_compute_node_options_py3 import FileGetFromComputeNodeOptions
    from .file_get_properties_from_compute_node_options_py3 import FileGetPropertiesFromComputeNodeOptions
    from .file_list_from_task_options_py3 import FileListFromTaskOptions
    from .file_list_from_compute_node_options_py3 import FileListFromComputeNodeOptions
    from .job_schedule_exists_options_py3 import JobScheduleExistsOptions
    from .job_schedule_delete_options_py3 import JobScheduleDeleteOptions
    from .job_schedule_get_options_py3 import JobScheduleGetOptions
    from .job_schedule_patch_options_py3 import JobSchedulePatchOptions
    from .job_schedule_update_options_py3 import JobScheduleUpdateOptions
    from .job_schedule_disable_options_py3 import JobScheduleDisableOptions
    from .job_schedule_enable_options_py3 import JobScheduleEnableOptions
    from .job_schedule_terminate_options_py3 import JobScheduleTerminateOptions
    from .job_schedule_add_options_py3 import JobScheduleAddOptions
    from .job_schedule_list_options_py3 import JobScheduleListOptions
    from .task_add_options_py3 import TaskAddOptions
    from .task_list_options_py3 import TaskListOptions
    from .task_add_collection_options_py3 import TaskAddCollectionOptions
    from .task_delete_options_py3 import TaskDeleteOptions
    from .task_get_options_py3 import TaskGetOptions
    from .task_update_options_py3 import TaskUpdateOptions
    from .task_list_subtasks_options_py3 import TaskListSubtasksOptions
    from .task_terminate_options_py3 import TaskTerminateOptions
    from .task_reactivate_options_py3 import TaskReactivateOptions
    from .compute_node_add_user_options_py3 import ComputeNodeAddUserOptions
    from .compute_node_delete_user_options_py3 import ComputeNodeDeleteUserOptions
    from .compute_node_update_user_options_py3 import ComputeNodeUpdateUserOptions
    from .compute_node_get_options_py3 import ComputeNodeGetOptions
    from .compute_node_reboot_options_py3 import ComputeNodeRebootOptions
    from .compute_node_reimage_options_py3 import ComputeNodeReimageOptions
    from .compute_node_disable_scheduling_options_py3 import ComputeNodeDisableSchedulingOptions
    from .compute_node_enable_scheduling_options_py3 import ComputeNodeEnableSchedulingOptions
    from .compute_node_get_remote_login_settings_options_py3 import ComputeNodeGetRemoteLoginSettingsOptions
    from .compute_node_get_remote_desktop_options_py3 import ComputeNodeGetRemoteDesktopOptions
    from .compute_node_upload_batch_service_logs_options_py3 import ComputeNodeUploadBatchServiceLogsOptions
    from .compute_node_list_options_py3 import ComputeNodeListOptions
except (SyntaxError, ImportError):
    from .pool_usage_metrics import PoolUsageMetrics
    from .image_reference import ImageReference
    from .image_information import ImageInformation
    from .authentication_token_settings import AuthenticationTokenSettings
    from .usage_statistics import UsageStatistics
    from .resource_statistics import ResourceStatistics
    from .pool_statistics import PoolStatistics
    from .job_statistics import JobStatistics
    from .name_value_pair import NameValuePair
    from .delete_certificate_error import DeleteCertificateError
    from .certificate import Certificate
    from .application_package_reference import ApplicationPackageReference
    from .application_summary import ApplicationSummary
    from .certificate_add_parameter import CertificateAddParameter
    from .file_properties import FileProperties
    from .node_file import NodeFile
    from .schedule import Schedule
    from .job_constraints import JobConstraints
    from .job_network_configuration import JobNetworkConfiguration
    from .container_registry import ContainerRegistry
    from .task_container_settings import TaskContainerSettings
    from .resource_file import ResourceFile
    from .environment_setting import EnvironmentSetting
    from .exit_options import ExitOptions
    from .exit_code_mapping import ExitCodeMapping
    from .exit_code_range_mapping import ExitCodeRangeMapping
    from .exit_conditions import ExitConditions
    from .auto_user_specification import AutoUserSpecification
    from .user_identity import UserIdentity
    from .linux_user_configuration import LinuxUserConfiguration
    from .windows_user_configuration import WindowsUserConfiguration
    from .user_account import UserAccount
    from .task_constraints import TaskConstraints
    from .output_file_blob_container_destination import OutputFileBlobContainerDestination
    from .output_file_destination import OutputFileDestination
    from .output_file_upload_options import OutputFileUploadOptions
    from .output_file import OutputFile
    from .job_manager_task import JobManagerTask
    from .job_preparation_task import JobPreparationTask
    from .job_release_task import JobReleaseTask
    from .task_scheduling_policy import TaskSchedulingPolicy
    from .start_task import StartTask
    from .certificate_reference import CertificateReference
    from .metadata_item import MetadataItem
    from .cloud_service_configuration import CloudServiceConfiguration
    from .windows_configuration import WindowsConfiguration
    from .data_disk import DataDisk
    from .container_configuration import ContainerConfiguration
    from .virtual_machine_configuration import VirtualMachineConfiguration
    from .network_security_group_rule import NetworkSecurityGroupRule
    from .inbound_nat_pool import InboundNATPool
    from .pool_endpoint_configuration import PoolEndpointConfiguration
    from .network_configuration import NetworkConfiguration
    from .azure_blob_file_system_configuration import AzureBlobFileSystemConfiguration
    from .nfs_mount_configuration import NFSMountConfiguration
    from .cifs_mount_configuration import CIFSMountConfiguration
    from .azure_file_share_configuration import AzureFileShareConfiguration
    from .mount_configuration import MountConfiguration
    from .pool_specification import PoolSpecification
    from .auto_pool_specification import AutoPoolSpecification
    from .pool_information import PoolInformation
    from .job_specification import JobSpecification
    from .recent_job import RecentJob
    from .job_schedule_execution_information import JobScheduleExecutionInformation
    from .job_schedule_statistics import JobScheduleStatistics
    from .cloud_job_schedule import CloudJobSchedule
    from .job_schedule_add_parameter import JobScheduleAddParameter
    from .job_scheduling_error import JobSchedulingError
    from .job_execution_information import JobExecutionInformation
    from .cloud_job import CloudJob
    from .job_add_parameter import JobAddParameter
    from .task_container_execution_information import TaskContainerExecutionInformation
    from .task_failure_information import TaskFailureInformation
    from .job_preparation_task_execution_information import JobPreparationTaskExecutionInformation
    from .job_release_task_execution_information import JobReleaseTaskExecutionInformation
    from .job_preparation_and_release_task_execution_information import JobPreparationAndReleaseTaskExecutionInformation
    from .task_counts import TaskCounts
    from .auto_scale_run_error import AutoScaleRunError
    from .auto_scale_run import AutoScaleRun
    from .resize_error import ResizeError
    from .cloud_pool import CloudPool
    from .pool_add_parameter import PoolAddParameter
    from .affinity_information import AffinityInformation
    from .task_execution_information import TaskExecutionInformation
    from .compute_node_information import ComputeNodeInformation
    from .node_agent_information import NodeAgentInformation
    from .multi_instance_settings import MultiInstanceSettings
    from .task_statistics import TaskStatistics
    from .task_id_range import TaskIdRange
    from .task_dependencies import TaskDependencies
    from .cloud_task import CloudTask
    from .task_add_parameter import TaskAddParameter
    from .task_add_collection_parameter import TaskAddCollectionParameter
    from .error_message import ErrorMessage
    from .batch_error_detail import BatchErrorDetail
    from .batch_error import BatchError, BatchErrorException
    from .task_add_result import TaskAddResult
    from .task_add_collection_result import TaskAddCollectionResult
    from .subtask_information import SubtaskInformation
    from .cloud_task_list_subtasks_result import CloudTaskListSubtasksResult
    from .task_information import TaskInformation
    from .start_task_information import StartTaskInformation
    from .compute_node_error import ComputeNodeError
    from .inbound_endpoint import InboundEndpoint
    from .compute_node_endpoint_configuration import ComputeNodeEndpointConfiguration
    from .compute_node import ComputeNode
    from .compute_node_user import ComputeNodeUser
    from .compute_node_get_remote_login_settings_result import ComputeNodeGetRemoteLoginSettingsResult
    from .job_schedule_patch_parameter import JobSchedulePatchParameter
    from .job_schedule_update_parameter import JobScheduleUpdateParameter
    from .job_disable_parameter import JobDisableParameter
    from .job_terminate_parameter import JobTerminateParameter
    from .job_patch_parameter import JobPatchParameter
    from .job_update_parameter import JobUpdateParameter
    from .pool_enable_auto_scale_parameter import PoolEnableAutoScaleParameter
    from .pool_evaluate_auto_scale_parameter import PoolEvaluateAutoScaleParameter
    from .pool_resize_parameter import PoolResizeParameter
    from .pool_update_properties_parameter import PoolUpdatePropertiesParameter
    from .pool_patch_parameter import PoolPatchParameter
    from .task_update_parameter import TaskUpdateParameter
    from .node_update_user_parameter import NodeUpdateUserParameter
    from .node_reboot_parameter import NodeRebootParameter
    from .node_reimage_parameter import NodeReimageParameter
    from .node_disable_scheduling_parameter import NodeDisableSchedulingParameter
    from .node_remove_parameter import NodeRemoveParameter
    from .upload_batch_service_logs_configuration import UploadBatchServiceLogsConfiguration
    from .upload_batch_service_logs_result import UploadBatchServiceLogsResult
    from .node_counts import NodeCounts
    from .pool_node_counts import PoolNodeCounts
    from .application_list_options import ApplicationListOptions
    from .application_get_options import ApplicationGetOptions
    from .pool_list_usage_metrics_options import PoolListUsageMetricsOptions
    from .pool_get_all_lifetime_statistics_options import PoolGetAllLifetimeStatisticsOptions
    from .pool_add_options import PoolAddOptions
    from .pool_list_options import PoolListOptions
    from .pool_delete_options import PoolDeleteOptions
    from .pool_exists_options import PoolExistsOptions
    from .pool_get_options import PoolGetOptions
    from .pool_patch_options import PoolPatchOptions
    from .pool_disable_auto_scale_options import PoolDisableAutoScaleOptions
    from .pool_enable_auto_scale_options import PoolEnableAutoScaleOptions
    from .pool_evaluate_auto_scale_options import PoolEvaluateAutoScaleOptions
    from .pool_resize_options import PoolResizeOptions
    from .pool_stop_resize_options import PoolStopResizeOptions
    from .pool_update_properties_options import PoolUpdatePropertiesOptions
    from .pool_remove_nodes_options import PoolRemoveNodesOptions
    from .account_list_supported_images_options import AccountListSupportedImagesOptions
    from .account_list_pool_node_counts_options import AccountListPoolNodeCountsOptions
    from .job_get_all_lifetime_statistics_options import JobGetAllLifetimeStatisticsOptions
    from .job_delete_options import JobDeleteOptions
    from .job_get_options import JobGetOptions
    from .job_patch_options import JobPatchOptions
    from .job_update_options import JobUpdateOptions
    from .job_disable_options import JobDisableOptions
    from .job_enable_options import JobEnableOptions
    from .job_terminate_options import JobTerminateOptions
    from .job_add_options import JobAddOptions
    from .job_list_options import JobListOptions
    from .job_list_from_job_schedule_options import JobListFromJobScheduleOptions
    from .job_list_preparation_and_release_task_status_options import JobListPreparationAndReleaseTaskStatusOptions
    from .job_get_task_counts_options import JobGetTaskCountsOptions
    from .certificate_add_options import CertificateAddOptions
    from .certificate_list_options import CertificateListOptions
    from .certificate_cancel_deletion_options import CertificateCancelDeletionOptions
    from .certificate_delete_options import CertificateDeleteOptions
    from .certificate_get_options import CertificateGetOptions
    from .file_delete_from_task_options import FileDeleteFromTaskOptions
    from .file_get_from_task_options import FileGetFromTaskOptions
    from .file_get_properties_from_task_options import FileGetPropertiesFromTaskOptions
    from .file_delete_from_compute_node_options import FileDeleteFromComputeNodeOptions
    from .file_get_from_compute_node_options import FileGetFromComputeNodeOptions
    from .file_get_properties_from_compute_node_options import FileGetPropertiesFromComputeNodeOptions
    from .file_list_from_task_options import FileListFromTaskOptions
    from .file_list_from_compute_node_options import FileListFromComputeNodeOptions
    from .job_schedule_exists_options import JobScheduleExistsOptions
    from .job_schedule_delete_options import JobScheduleDeleteOptions
    from .job_schedule_get_options import JobScheduleGetOptions
    from .job_schedule_patch_options import JobSchedulePatchOptions
    from .job_schedule_update_options import JobScheduleUpdateOptions
    from .job_schedule_disable_options import JobScheduleDisableOptions
    from .job_schedule_enable_options import JobScheduleEnableOptions
    from .job_schedule_terminate_options import JobScheduleTerminateOptions
    from .job_schedule_add_options import JobScheduleAddOptions
    from .job_schedule_list_options import JobScheduleListOptions
    from .task_add_options import TaskAddOptions
    from .task_list_options import TaskListOptions
    from .task_add_collection_options import TaskAddCollectionOptions
    from .task_delete_options import TaskDeleteOptions
    from .task_get_options import TaskGetOptions
    from .task_update_options import TaskUpdateOptions
    from .task_list_subtasks_options import TaskListSubtasksOptions
    from .task_terminate_options import TaskTerminateOptions
    from .task_reactivate_options import TaskReactivateOptions
    from .compute_node_add_user_options import ComputeNodeAddUserOptions
    from .compute_node_delete_user_options import ComputeNodeDeleteUserOptions
    from .compute_node_update_user_options import ComputeNodeUpdateUserOptions
    from .compute_node_get_options import ComputeNodeGetOptions
    from .compute_node_reboot_options import ComputeNodeRebootOptions
    from .compute_node_reimage_options import ComputeNodeReimageOptions
    from .compute_node_disable_scheduling_options import ComputeNodeDisableSchedulingOptions
    from .compute_node_enable_scheduling_options import ComputeNodeEnableSchedulingOptions
    from .compute_node_get_remote_login_settings_options import ComputeNodeGetRemoteLoginSettingsOptions
    from .compute_node_get_remote_desktop_options import ComputeNodeGetRemoteDesktopOptions
    from .compute_node_upload_batch_service_logs_options import ComputeNodeUploadBatchServiceLogsOptions
    from .compute_node_list_options import ComputeNodeListOptions
from .application_summary_paged import ApplicationSummaryPaged
from .pool_usage_metrics_paged import PoolUsageMetricsPaged
from .cloud_pool_paged import CloudPoolPaged
from .image_information_paged import ImageInformationPaged
from .pool_node_counts_paged import PoolNodeCountsPaged
from .cloud_job_paged import CloudJobPaged
from .job_preparation_and_release_task_execution_information_paged import JobPreparationAndReleaseTaskExecutionInformationPaged
from .certificate_paged import CertificatePaged
from .node_file_paged import NodeFilePaged
from .cloud_job_schedule_paged import CloudJobSchedulePaged
from .cloud_task_paged import CloudTaskPaged
from .compute_node_paged import ComputeNodePaged
from .batch_service_client_enums import (
    OSType,
    VerificationType,
    AccessScope,
    CertificateState,
    CertificateFormat,
    ContainerWorkingDirectory,
    JobAction,
    DependencyAction,
    AutoUserScope,
    ElevationLevel,
    LoginMode,
    OutputFileUploadCondition,
    ComputeNodeFillType,
    CertificateStoreLocation,
    CertificateVisibility,
    CachingType,
    StorageAccountType,
    DynamicVNetAssignmentScope,
    InboundEndpointProtocol,
    NetworkSecurityGroupRuleAccess,
    PoolLifetimeOption,
    OnAllTasksComplete,
    OnTaskFailure,
    JobScheduleState,
    ErrorCategory,
    JobState,
    JobPreparationTaskState,
    TaskExecutionResult,
    JobReleaseTaskState,
    PoolState,
    AllocationState,
    TaskState,
    TaskAddStatus,
    SubtaskState,
    StartTaskState,
    ComputeNodeState,
    SchedulingState,
    DisableJobOption,
    ComputeNodeDeallocationOption,
    ComputeNodeRebootOption,
    ComputeNodeReimageOption,
    DisableComputeNodeSchedulingOption,
)

__all__ = [
    'PoolUsageMetrics',
    'ImageReference',
    'ImageInformation',
    'AuthenticationTokenSettings',
    'UsageStatistics',
    'ResourceStatistics',
    'PoolStatistics',
    'JobStatistics',
    'NameValuePair',
    'DeleteCertificateError',
    'Certificate',
    'ApplicationPackageReference',
    'ApplicationSummary',
    'CertificateAddParameter',
    'FileProperties',
    'NodeFile',
    'Schedule',
    'JobConstraints',
    'JobNetworkConfiguration',
    'ContainerRegistry',
    'TaskContainerSettings',
    'ResourceFile',
    'EnvironmentSetting',
    'ExitOptions',
    'ExitCodeMapping',
    'ExitCodeRangeMapping',
    'ExitConditions',
    'AutoUserSpecification',
    'UserIdentity',
    'LinuxUserConfiguration',
    'WindowsUserConfiguration',
    'UserAccount',
    'TaskConstraints',
    'OutputFileBlobContainerDestination',
    'OutputFileDestination',
    'OutputFileUploadOptions',
    'OutputFile',
    'JobManagerTask',
    'JobPreparationTask',
    'JobReleaseTask',
    'TaskSchedulingPolicy',
    'StartTask',
    'CertificateReference',
    'MetadataItem',
    'CloudServiceConfiguration',
    'WindowsConfiguration',
    'DataDisk',
    'ContainerConfiguration',
    'VirtualMachineConfiguration',
    'NetworkSecurityGroupRule',
    'InboundNATPool',
    'PoolEndpointConfiguration',
    'NetworkConfiguration',
    'AzureBlobFileSystemConfiguration',
    'NFSMountConfiguration',
    'CIFSMountConfiguration',
    'AzureFileShareConfiguration',
    'MountConfiguration',
    'PoolSpecification',
    'AutoPoolSpecification',
    'PoolInformation',
    'JobSpecification',
    'RecentJob',
    'JobScheduleExecutionInformation',
    'JobScheduleStatistics',
    'CloudJobSchedule',
    'JobScheduleAddParameter',
    'JobSchedulingError',
    'JobExecutionInformation',
    'CloudJob',
    'JobAddParameter',
    'TaskContainerExecutionInformation',
    'TaskFailureInformation',
    'JobPreparationTaskExecutionInformation',
    'JobReleaseTaskExecutionInformation',
    'JobPreparationAndReleaseTaskExecutionInformation',
    'TaskCounts',
    'AutoScaleRunError',
    'AutoScaleRun',
    'ResizeError',
    'CloudPool',
    'PoolAddParameter',
    'AffinityInformation',
    'TaskExecutionInformation',
    'ComputeNodeInformation',
    'NodeAgentInformation',
    'MultiInstanceSettings',
    'TaskStatistics',
    'TaskIdRange',
    'TaskDependencies',
    'CloudTask',
    'TaskAddParameter',
    'TaskAddCollectionParameter',
    'ErrorMessage',
    'BatchErrorDetail',
    'BatchError', 'BatchErrorException',
    'TaskAddResult',
    'TaskAddCollectionResult',
    'SubtaskInformation',
    'CloudTaskListSubtasksResult',
    'TaskInformation',
    'StartTaskInformation',
    'ComputeNodeError',
    'InboundEndpoint',
    'ComputeNodeEndpointConfiguration',
    'ComputeNode',
    'ComputeNodeUser',
    'ComputeNodeGetRemoteLoginSettingsResult',
    'JobSchedulePatchParameter',
    'JobScheduleUpdateParameter',
    'JobDisableParameter',
    'JobTerminateParameter',
    'JobPatchParameter',
    'JobUpdateParameter',
    'PoolEnableAutoScaleParameter',
    'PoolEvaluateAutoScaleParameter',
    'PoolResizeParameter',
    'PoolUpdatePropertiesParameter',
    'PoolPatchParameter',
    'TaskUpdateParameter',
    'NodeUpdateUserParameter',
    'NodeRebootParameter',
    'NodeReimageParameter',
    'NodeDisableSchedulingParameter',
    'NodeRemoveParameter',
    'UploadBatchServiceLogsConfiguration',
    'UploadBatchServiceLogsResult',
    'NodeCounts',
    'PoolNodeCounts',
    'ApplicationListOptions',
    'ApplicationGetOptions',
    'PoolListUsageMetricsOptions',
    'PoolGetAllLifetimeStatisticsOptions',
    'PoolAddOptions',
    'PoolListOptions',
    'PoolDeleteOptions',
    'PoolExistsOptions',
    'PoolGetOptions',
    'PoolPatchOptions',
    'PoolDisableAutoScaleOptions',
    'PoolEnableAutoScaleOptions',
    'PoolEvaluateAutoScaleOptions',
    'PoolResizeOptions',
    'PoolStopResizeOptions',
    'PoolUpdatePropertiesOptions',
    'PoolRemoveNodesOptions',
    'AccountListSupportedImagesOptions',
    'AccountListPoolNodeCountsOptions',
    'JobGetAllLifetimeStatisticsOptions',
    'JobDeleteOptions',
    'JobGetOptions',
    'JobPatchOptions',
    'JobUpdateOptions',
    'JobDisableOptions',
    'JobEnableOptions',
    'JobTerminateOptions',
    'JobAddOptions',
    'JobListOptions',
    'JobListFromJobScheduleOptions',
    'JobListPreparationAndReleaseTaskStatusOptions',
    'JobGetTaskCountsOptions',
    'CertificateAddOptions',
    'CertificateListOptions',
    'CertificateCancelDeletionOptions',
    'CertificateDeleteOptions',
    'CertificateGetOptions',
    'FileDeleteFromTaskOptions',
    'FileGetFromTaskOptions',
    'FileGetPropertiesFromTaskOptions',
    'FileDeleteFromComputeNodeOptions',
    'FileGetFromComputeNodeOptions',
    'FileGetPropertiesFromComputeNodeOptions',
    'FileListFromTaskOptions',
    'FileListFromComputeNodeOptions',
    'JobScheduleExistsOptions',
    'JobScheduleDeleteOptions',
    'JobScheduleGetOptions',
    'JobSchedulePatchOptions',
    'JobScheduleUpdateOptions',
    'JobScheduleDisableOptions',
    'JobScheduleEnableOptions',
    'JobScheduleTerminateOptions',
    'JobScheduleAddOptions',
    'JobScheduleListOptions',
    'TaskAddOptions',
    'TaskListOptions',
    'TaskAddCollectionOptions',
    'TaskDeleteOptions',
    'TaskGetOptions',
    'TaskUpdateOptions',
    'TaskListSubtasksOptions',
    'TaskTerminateOptions',
    'TaskReactivateOptions',
    'ComputeNodeAddUserOptions',
    'ComputeNodeDeleteUserOptions',
    'ComputeNodeUpdateUserOptions',
    'ComputeNodeGetOptions',
    'ComputeNodeRebootOptions',
    'ComputeNodeReimageOptions',
    'ComputeNodeDisableSchedulingOptions',
    'ComputeNodeEnableSchedulingOptions',
    'ComputeNodeGetRemoteLoginSettingsOptions',
    'ComputeNodeGetRemoteDesktopOptions',
    'ComputeNodeUploadBatchServiceLogsOptions',
    'ComputeNodeListOptions',
    'ApplicationSummaryPaged',
    'PoolUsageMetricsPaged',
    'CloudPoolPaged',
    'ImageInformationPaged',
    'PoolNodeCountsPaged',
    'CloudJobPaged',
    'JobPreparationAndReleaseTaskExecutionInformationPaged',
    'CertificatePaged',
    'NodeFilePaged',
    'CloudJobSchedulePaged',
    'CloudTaskPaged',
    'ComputeNodePaged',
    'OSType',
    'VerificationType',
    'AccessScope',
    'CertificateState',
    'CertificateFormat',
    'ContainerWorkingDirectory',
    'JobAction',
    'DependencyAction',
    'AutoUserScope',
    'ElevationLevel',
    'LoginMode',
    'OutputFileUploadCondition',
    'ComputeNodeFillType',
    'CertificateStoreLocation',
    'CertificateVisibility',
    'CachingType',
    'StorageAccountType',
    'DynamicVNetAssignmentScope',
    'InboundEndpointProtocol',
    'NetworkSecurityGroupRuleAccess',
    'PoolLifetimeOption',
    'OnAllTasksComplete',
    'OnTaskFailure',
    'JobScheduleState',
    'ErrorCategory',
    'JobState',
    'JobPreparationTaskState',
    'TaskExecutionResult',
    'JobReleaseTaskState',
    'PoolState',
    'AllocationState',
    'TaskState',
    'TaskAddStatus',
    'SubtaskState',
    'StartTaskState',
    'ComputeNodeState',
    'SchedulingState',
    'DisableJobOption',
    'ComputeNodeDeallocationOption',
    'ComputeNodeRebootOption',
    'ComputeNodeReimageOption',
    'DisableComputeNodeSchedulingOption',
]
