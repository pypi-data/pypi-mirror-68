# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetPolicySetDefinitionResult:
    """
    A collection of values returned by getPolicySetDefinition.
    """
    def __init__(__self__, description=None, display_name=None, id=None, management_group_name=None, metadata=None, name=None, parameters=None, policy_definitions=None, policy_type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        __self__.description = description
        """
        The Description of the Policy Set Definition.
        """
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        __self__.display_name = display_name
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if management_group_name and not isinstance(management_group_name, str):
            raise TypeError("Expected argument 'management_group_name' to be a str")
        __self__.management_group_name = management_group_name
        if metadata and not isinstance(metadata, str):
            raise TypeError("Expected argument 'metadata' to be a str")
        __self__.metadata = metadata
        """
        Any Metadata defined in the Policy Set Definition.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if parameters and not isinstance(parameters, str):
            raise TypeError("Expected argument 'parameters' to be a str")
        __self__.parameters = parameters
        """
        Any Parameters defined in the Policy Set Definition.
        """
        if policy_definitions and not isinstance(policy_definitions, str):
            raise TypeError("Expected argument 'policy_definitions' to be a str")
        __self__.policy_definitions = policy_definitions
        """
        The policy definitions contained within the policy set definition.
        """
        if policy_type and not isinstance(policy_type, str):
            raise TypeError("Expected argument 'policy_type' to be a str")
        __self__.policy_type = policy_type
        """
        The Type of the Policy Set Definition.
        """
class AwaitableGetPolicySetDefinitionResult(GetPolicySetDefinitionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicySetDefinitionResult(
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            management_group_name=self.management_group_name,
            metadata=self.metadata,
            name=self.name,
            parameters=self.parameters,
            policy_definitions=self.policy_definitions,
            policy_type=self.policy_type)

def get_policy_set_definition(display_name=None,management_group_name=None,name=None,opts=None):
    """
    Use this data source to access information about an existing Policy Set Definition.




    :param str display_name: Specifies the display name of the Policy Set Definition. Conflicts with `name`.
    :param str management_group_name: Only retrieve Policy Set Definitions from this Management Group.
    :param str name: Specifies the name of the Policy Set Definition. Conflicts with `display_name`.
    """
    __args__ = dict()


    __args__['displayName'] = display_name
    __args__['managementGroupName'] = management_group_name
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:policy/getPolicySetDefinition:getPolicySetDefinition', __args__, opts=opts).value

    return AwaitableGetPolicySetDefinitionResult(
        description=__ret__.get('description'),
        display_name=__ret__.get('displayName'),
        id=__ret__.get('id'),
        management_group_name=__ret__.get('managementGroupName'),
        metadata=__ret__.get('metadata'),
        name=__ret__.get('name'),
        parameters=__ret__.get('parameters'),
        policy_definitions=__ret__.get('policyDefinitions'),
        policy_type=__ret__.get('policyType'))
