# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class NetworkInterfaceNatRuleAssociation(pulumi.CustomResource):
    ip_configuration_name: pulumi.Output[str]
    """
    The Name of the IP Configuration within the Network Interface which should be connected to the NAT Rule. Changing this forces a new resource to be created.
    """
    nat_rule_id: pulumi.Output[str]
    """
    The ID of the Load Balancer NAT Rule which this Network Interface which should be connected to. Changing this forces a new resource to be created.
    """
    network_interface_id: pulumi.Output[str]
    """
    The ID of the Network Interface. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, ip_configuration_name=None, nat_rule_id=None, network_interface_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages the association between a Network Interface and a Load Balancer's NAT Rule.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_configuration_name: The Name of the IP Configuration within the Network Interface which should be connected to the NAT Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] nat_rule_id: The ID of the Load Balancer NAT Rule which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if ip_configuration_name is None:
                raise TypeError("Missing required property 'ip_configuration_name'")
            __props__['ip_configuration_name'] = ip_configuration_name
            if nat_rule_id is None:
                raise TypeError("Missing required property 'nat_rule_id'")
            __props__['nat_rule_id'] = nat_rule_id
            if network_interface_id is None:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__['network_interface_id'] = network_interface_id
        super(NetworkInterfaceNatRuleAssociation, __self__).__init__(
            'azure:network/networkInterfaceNatRuleAssociation:NetworkInterfaceNatRuleAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, ip_configuration_name=None, nat_rule_id=None, network_interface_id=None):
        """
        Get an existing NetworkInterfaceNatRuleAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ip_configuration_name: The Name of the IP Configuration within the Network Interface which should be connected to the NAT Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] nat_rule_id: The ID of the Load Balancer NAT Rule which this Network Interface which should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] network_interface_id: The ID of the Network Interface. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["ip_configuration_name"] = ip_configuration_name
        __props__["nat_rule_id"] = nat_rule_id
        __props__["network_interface_id"] = network_interface_id
        return NetworkInterfaceNatRuleAssociation(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

