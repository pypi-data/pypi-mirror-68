# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetNetworkSecurityGroupResult:
    """
    A collection of values returned by getNetworkSecurityGroup.
    """
    def __init__(__self__, id=None, location=None, name=None, resource_group_name=None, security_rules=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The supported Azure location where the resource exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        """
        The name of the security rule.
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if security_rules and not isinstance(security_rules, list):
            raise TypeError("Expected argument 'security_rules' to be a list")
        __self__.security_rules = security_rules
        """
        One or more `security_rule` blocks as defined below.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
class AwaitableGetNetworkSecurityGroupResult(GetNetworkSecurityGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkSecurityGroupResult(
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            security_rules=self.security_rules,
            tags=self.tags)

def get_network_security_group(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Network Security Group.




    :param str name: Specifies the Name of the Network Security Group.
    :param str resource_group_name: Specifies the Name of the Resource Group within which the Network Security Group exists
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:network/getNetworkSecurityGroup:getNetworkSecurityGroup', __args__, opts=opts).value

    return AwaitableGetNetworkSecurityGroupResult(
        id=__ret__.get('id'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        security_rules=__ret__.get('securityRules'),
        tags=__ret__.get('tags'))
