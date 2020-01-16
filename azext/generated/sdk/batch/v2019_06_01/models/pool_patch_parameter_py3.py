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


class PoolPatchParameter(Model):
    """The set of changes to be made to a Pool.

    :param start_task: A Task to run on each Compute Node as it joins the
     Pool. The Task runs when the Compute Node is added to the Pool or when the
     Compute Node is restarted. If this element is present, it overwrites any
     existing start Task. If omitted, any existing start Task is left
     unchanged.
    :type start_task: ~azure.batch.models.StartTask
    :param certificate_references: A list of Certificates to be installed on
     each Compute Node in the Pool. If this element is present, it replaces any
     existing Certificate references configured on the Pool. If omitted, any
     existing Certificate references are left unchanged. For Windows Nodes, the
     Batch service installs the Certificates to the specified Certificate store
     and location. For Linux Compute Nodes, the Certificates are stored in a
     directory inside the Task working directory and an environment variable
     AZ_BATCH_CERTIFICATES_DIR is supplied to the Task to query for this
     location. For Certificates with visibility of 'remoteUser', a 'certs'
     directory is created in the user's home directory (e.g.,
     /home/{user-name}/certs) and Certificates are placed in that directory.
    :type certificate_references:
     list[~azure.batch.models.CertificateReference]
    :param application_package_references: A list of Packages to be installed
     on each Compute Node in the Pool. Changes to Package references affect all
     new Nodes joining the Pool, but do not affect Compute Nodes that are
     already in the Pool until they are rebooted or reimaged. If this element
     is present, it replaces any existing Package references. If you specify an
     empty collection, then all Package references are removed from the Pool.
     If omitted, any existing Package references are left unchanged.
    :type application_package_references:
     list[~azure.batch.models.ApplicationPackageReference]
    :param metadata: A list of name-value pairs associated with the Pool as
     metadata. If this element is present, it replaces any existing metadata
     configured on the Pool. If you specify an empty collection, any metadata
     is removed from the Pool. If omitted, any existing metadata is left
     unchanged.
    :type metadata: list[~azure.batch.models.MetadataItem]
    """

    _attribute_map = {
        'start_task': {'key': 'startTask', 'type': 'StartTask'},
        'certificate_references': {'key': 'certificateReferences', 'type': '[CertificateReference]'},
        'application_package_references': {'key': 'applicationPackageReferences', 'type': '[ApplicationPackageReference]'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
    }

    def __init__(self, *, start_task=None, certificate_references=None, application_package_references=None, metadata=None, **kwargs) -> None:
        super(PoolPatchParameter, self).__init__(**kwargs)
        self.start_task = start_task
        self.certificate_references = certificate_references
        self.application_package_references = application_package_references
        self.metadata = metadata
