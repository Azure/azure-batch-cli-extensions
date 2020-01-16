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


class ImageReference(Model):
    """A reference to an Azure Virtual Machines Marketplace Image or a custom
    Azure Virtual Machine Image. To get the list of all Azure Marketplace Image
    references verified by Azure Batch, see the 'List supported Images'
    operation.

    :param publisher: The publisher of the Azure Virtual Machines Marketplace
     Image. For example, Canonical or MicrosoftWindowsServer.
    :type publisher: str
    :param offer: The offer type of the Azure Virtual Machines Marketplace
     Image. For example, UbuntuServer or WindowsServer.
    :type offer: str
    :param sku: The SKU of the Azure Virtual Machines Marketplace Image. For
     example, 18.04-LTS or 2019-Datacenter.
    :type sku: str
    :param version: The version of the Azure Virtual Machines Marketplace
     Image. A value of 'latest' can be specified to select the latest version
     of an Image. If omitted, the default is 'latest'.
    :type version: str
    :param virtual_machine_image_id: The ARM resource identifier of the
     Virtual Machine Image or Shared Image Gallery Image. Computes Compute
     Nodes of the Pool will be created using this Image Id. This is of either
     the form
     /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/images/{imageName}
     for Virtual Machine Image or
     /subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/galleries/{galleryName}/images/{imageDefinitionName}/versions/{versionId}
     for SIG image. This property is mutually exclusive with other
     ImageReference properties. For Virtual Machine Image it must be in the
     same region and subscription as the Azure Batch account. For SIG image it
     must have replicas in the same region as the Azure Batch account. For
     information about the firewall settings for the Batch Compute Node agent
     to communicate with the Batch service see
     https://docs.microsoft.com/en-us/azure/batch/batch-api-basics#virtual-network-vnet-and-firewall-configuration.
    :type virtual_machine_image_id: str
    """

    _attribute_map = {
        'publisher': {'key': 'publisher', 'type': 'str'},
        'offer': {'key': 'offer', 'type': 'str'},
        'sku': {'key': 'sku', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'virtual_machine_image_id': {'key': 'virtualMachineImageId', 'type': 'str'},
    }

    def __init__(self, *, publisher: str=None, offer: str=None, sku: str=None, version: str=None, virtual_machine_image_id: str=None, **kwargs) -> None:
        super(ImageReference, self).__init__(**kwargs)
        self.publisher = publisher
        self.offer = offer
        self.sku = sku
        self.version = version
        self.virtual_machine_image_id = virtual_machine_image_id
