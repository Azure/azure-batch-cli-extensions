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


class PoolUsageMetrics(Model):
    """Usage metrics for a Pool across an aggregation interval.

    All required parameters must be populated in order to send to Azure.

    :param pool_id: Required. The ID of the Pool whose metrics are aggregated
     in this entry.
    :type pool_id: str
    :param start_time: Required. The start time of the aggregation interval
     covered by this entry.
    :type start_time: datetime
    :param end_time: Required. The end time of the aggregation interval
     covered by this entry.
    :type end_time: datetime
    :param vm_size: Required. The size of virtual machines in the Pool. All
     VMs in a Pool are the same size. For information about available sizes of
     virtual machines in Pools, see Choose a VM size for Compute Nodes in an
     Azure Batch Pool
     (https://docs.microsoft.com/azure/batch/batch-pool-vm-sizes).
    :type vm_size: str
    :param total_core_hours: Required. The total core hours used in the Pool
     during this aggregation interval.
    :type total_core_hours: float
    """

    _validation = {
        'pool_id': {'required': True},
        'start_time': {'required': True},
        'end_time': {'required': True},
        'vm_size': {'required': True},
        'total_core_hours': {'required': True},
    }

    _attribute_map = {
        'pool_id': {'key': 'poolId', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'vm_size': {'key': 'vmSize', 'type': 'str'},
        'total_core_hours': {'key': 'totalCoreHours', 'type': 'float'},
    }

    def __init__(self, **kwargs):
        super(PoolUsageMetrics, self).__init__(**kwargs)
        self.pool_id = kwargs.get('pool_id', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.vm_size = kwargs.get('vm_size', None)
        self.total_core_hours = kwargs.get('total_core_hours', None)
