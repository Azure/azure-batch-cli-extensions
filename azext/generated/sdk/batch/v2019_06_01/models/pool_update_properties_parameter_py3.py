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


class PoolUpdatePropertiesParameter(Model):
    """The set of changes to be made to a Pool.

    All required parameters must be populated in order to send to Azure.

    :param start_task: A Task to run on each Compute Node as it joins the
     Pool. The Task runs when the Compute Node is added to the Pool or when the
     Compute Node is restarted. If this element is present, it overwrites any
     existing start Task. If omitted, any existing start Task is removed from
     the Pool.
    :type start_task: ~azure.batch.models.StartTask
    :param certificate_references: Required. A list of Certificates to be
     installed on each Compute Node in the Pool. This list replaces any
     existing Certificate references configured on the Pool. If you specify an
     empty collection, any existing Certificate references are removed from the
     Pool. For Windows Nodes, the Batch service installs the Certificates to
     the specified Certificate store and location. For Linux Compute Nodes, the
     Certificates are stored in a directory inside the Task working directory
     and an environment variable AZ_BATCH_CERTIFICATES_DIR is supplied to the
     Task to query for this location. For Certificates with visibility of
     'remoteUser', a 'certs' directory is created in the user's home directory
     (e.g., /home/{user-name}/certs) and Certificates are placed in that
     directory.
    :type certificate_references:
     list[~azure.batch.models.CertificateReference]
    :param application_package_references: Required. The list of Application
     Packages to be installed on each Compute Node in the Pool. The list
     replaces any existing Application Package references on the Pool. Changes
     to Application Package references affect all new Compute Nodes joining the
     Pool, but do not affect Compute Nodes that are already in the Pool until
     they are rebooted or reimaged. There is a maximum of 10 Application
     Package references on any given Pool. If omitted, or if you specify an
     empty collection, any existing Application Packages references are removed
     from the Pool. A maximum of 10 references may be specified on a given
     Pool.
    :type application_package_references:
     list[~azure.batch.models.ApplicationPackageReference]
    :param metadata: Required. A list of name-value pairs associated with the
     Pool as metadata. This list replaces any existing metadata configured on
     the Pool. If omitted, or if you specify an empty collection, any existing
     metadata is removed from the Pool.
    :type metadata: list[~azure.batch.models.MetadataItem]
    """

    _validation = {
        'certificate_references': {'required': True},
        'application_package_references': {'required': True},
        'metadata': {'required': True},
    }

    _attribute_map = {
        'start_task': {'key': 'startTask', 'type': 'StartTask'},
        'certificate_references': {'key': 'certificateReferences', 'type': '[CertificateReference]'},
        'application_package_references': {'key': 'applicationPackageReferences', 'type': '[ApplicationPackageReference]'},
        'metadata': {'key': 'metadata', 'type': '[MetadataItem]'},
    }

    def __init__(self, *, certificate_references, application_package_references, metadata, start_task=None, **kwargs) -> None:
        super(PoolUpdatePropertiesParameter, self).__init__(**kwargs)
        self.start_task = start_task
        self.certificate_references = certificate_references
        self.application_package_references = application_package_references
        self.metadata = metadata
