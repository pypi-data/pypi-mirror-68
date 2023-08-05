# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetServerResult:
    """
    A collection of values returned by getServer.
    """
    def __init__(__self__, administrator_login=None, fqdn=None, id=None, identities=None, location=None, name=None, resource_group_name=None, tags=None, version=None):
        if administrator_login and not isinstance(administrator_login, str):
            raise TypeError("Expected argument 'administrator_login' to be a str")
        __self__.administrator_login = administrator_login
        """
        The administrator username of the SQL Server.
        """
        if fqdn and not isinstance(fqdn, str):
            raise TypeError("Expected argument 'fqdn' to be a str")
        __self__.fqdn = fqdn
        """
        The fully qualified domain name of the SQL Server.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if identities and not isinstance(identities, list):
            raise TypeError("Expected argument 'identities' to be a list")
        __self__.identities = identities
        """
        An `identity` block as defined below.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The location of the Resource Group in which the SQL Server exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags assigned to the resource.
        """
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        __self__.version = version
        """
        The version of the SQL Server.
        """
class AwaitableGetServerResult(GetServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServerResult(
            administrator_login=self.administrator_login,
            fqdn=self.fqdn,
            id=self.id,
            identities=self.identities,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            tags=self.tags,
            version=self.version)

def get_server(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing SQL Azure Database Server.




    :param str name: The name of the SQL Server.
    :param str resource_group_name: Specifies the name of the Resource Group where the SQL Server exists.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:sql/getServer:getServer', __args__, opts=opts).value

    return AwaitableGetServerResult(
        administrator_login=__ret__.get('administratorLogin'),
        fqdn=__ret__.get('fqdn'),
        id=__ret__.get('id'),
        identities=__ret__.get('identities'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        resource_group_name=__ret__.get('resourceGroupName'),
        tags=__ret__.get('tags'),
        version=__ret__.get('version'))
