# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetStorageContainerResult:
    """
    A collection of values returned by getStorageContainer.
    """
    def __init__(__self__, container_access_type=None, has_immutability_policy=None, has_legal_hold=None, id=None, metadata=None, name=None, resource_manager_id=None, storage_account_name=None):
        if container_access_type and not isinstance(container_access_type, str):
            raise TypeError("Expected argument 'container_access_type' to be a str")
        __self__.container_access_type = container_access_type
        """
        The Access Level configured for this Container.
        """
        if has_immutability_policy and not isinstance(has_immutability_policy, bool):
            raise TypeError("Expected argument 'has_immutability_policy' to be a bool")
        __self__.has_immutability_policy = has_immutability_policy
        """
        Is there an Immutability Policy configured on this Storage Container?
        """
        if has_legal_hold and not isinstance(has_legal_hold, bool):
            raise TypeError("Expected argument 'has_legal_hold' to be a bool")
        __self__.has_legal_hold = has_legal_hold
        """
        Is there a Legal Hold configured on this Storage Container?
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        __self__.metadata = metadata
        """
        A mapping of MetaData for this Container.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_manager_id and not isinstance(resource_manager_id, str):
            raise TypeError("Expected argument 'resource_manager_id' to be a str")
        __self__.resource_manager_id = resource_manager_id
        """
        The Resource Manager ID of this Storage Container.
        """
        if storage_account_name and not isinstance(storage_account_name, str):
            raise TypeError("Expected argument 'storage_account_name' to be a str")
        __self__.storage_account_name = storage_account_name
class AwaitableGetStorageContainerResult(GetStorageContainerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageContainerResult(
            container_access_type=self.container_access_type,
            has_immutability_policy=self.has_immutability_policy,
            has_legal_hold=self.has_legal_hold,
            id=self.id,
            metadata=self.metadata,
            name=self.name,
            resource_manager_id=self.resource_manager_id,
            storage_account_name=self.storage_account_name)

def get_storage_container(metadata=None,name=None,storage_account_name=None,opts=None):
    """
    Use this data source to access information about an existing Storage Container.




    :param dict metadata: A mapping of MetaData for this Container.
    :param str name: The name of the Container.
    :param str storage_account_name: The name of the Storage Account where the Container exists.
    """
    __args__ = dict()


    __args__['metadata'] = metadata
    __args__['name'] = name
    __args__['storageAccountName'] = storage_account_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:storage/getStorageContainer:getStorageContainer', __args__, opts=opts).value

    return AwaitableGetStorageContainerResult(
        container_access_type=__ret__.get('containerAccessType'),
        has_immutability_policy=__ret__.get('hasImmutabilityPolicy'),
        has_legal_hold=__ret__.get('hasLegalHold'),
        id=__ret__.get('id'),
        metadata=__ret__.get('metadata'),
        name=__ret__.get('name'),
        resource_manager_id=__ret__.get('resourceManagerId'),
        storage_account_name=__ret__.get('storageAccountName'))
