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


class JobSchedulePatchParameter(Model):
    """The set of changes to be made to a Job Schedule.

    :param schedule: The schedule according to which Jobs will be created. If
     you do not specify this element, the existing schedule is left unchanged.
    :type schedule: ~azure.batch.models.Schedule
    :param job_specification: The details of the Jobs to be created on this
     schedule. Updates affect only Jobs that are started after the update has
     taken place. Any currently active Job continues with the older
     specification.
    :type job_specification: ~azure.batch.models.JobSpecification
    :param metadata: A list of name-value pairs associated with the Job
     Schedule as metadata. If you do not specify this element, existing
     metadata is left unchanged.
    :type metadata: list[~azure.batch.models.MetadataItem]
    """

    _attribute_map = {
        'schedule': {'key': 'schedule', 'type': 'Schedule'},
        'job_specification': {'key': 'jobSpecification', 'type': 'JobSpecification'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
    }

    def __init__(self, **kwargs):
        super(JobSchedulePatchParameter, self).__init__(**kwargs)
        self.schedule = kwargs.get('schedule', None)
        self.job_specification = kwargs.get('job_specification', None)
        self.metadata = kwargs.get('metadata', None)
