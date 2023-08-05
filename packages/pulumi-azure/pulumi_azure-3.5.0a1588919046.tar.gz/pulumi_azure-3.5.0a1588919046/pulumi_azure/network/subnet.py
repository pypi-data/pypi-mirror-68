# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Subnet(pulumi.CustomResource):
    address_prefix: pulumi.Output[str]
    """
    The address prefix to use for the subnet.
    """
    address_prefixes: pulumi.Output[list]
    """
    The address prefixes to use for the subnet.
    """
    delegations: pulumi.Output[list]
    """
    One or more `delegation` blocks as defined below.

      * `name` (`str`) - A name for this delegation.
      * `serviceDelegation` (`dict`) - A `service_delegation` block as defined below.
        * `actions` (`list`) - A list of Actions which should be delegated. This list is specific to the service to delegate to. Possible values include `Microsoft.Network/networkinterfaces/*`, `Microsoft.Network/virtualNetworks/subnets/action`, `Microsoft.Network/virtualNetworks/subnets/join/action`, `Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action` and `Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action`.
        * `name` (`str`) - The name of service to delegate to. Possible values include `Microsoft.BareMetal/AzureVMware`, `Microsoft.BareMetal/CrayServers`, `Microsoft.Batch/batchAccounts`, `Microsoft.ContainerInstance/containerGroups`, `Microsoft.Databricks/workspaces`, `Microsoft.DBforPostgreSQL/serversv2`, `Microsoft.HardwareSecurityModules/dedicatedHSMs`, `Microsoft.Logic/integrationServiceEnvironments`, `Microsoft.Netapp/volumes`, `Microsoft.ServiceFabricMesh/networks`, `Microsoft.Sql/managedInstances`, `Microsoft.Sql/servers`, `Microsoft.StreamAnalytics/streamingJobs`, `Microsoft.Web/hostingEnvironments` and `Microsoft.Web/serverFarms`.
    """
    enforce_private_link_endpoint_network_policies: pulumi.Output[bool]
    """
    Enable or Disable network policies for the private link endpoint on the subnet. Default value is `false`. Conflicts with enforce_private_link_service_network_policies.
    """
    enforce_private_link_service_network_policies: pulumi.Output[bool]
    """
    Enable or Disable network policies for the private link service on the subnet. Default valule is `false`. Conflicts with `enforce_private_link_endpoint_network_policies`.
    """
    name: pulumi.Output[str]
    """
    The name of the subnet. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the subnet. Changing this forces a new resource to be created.
    """
    service_endpoints: pulumi.Output[list]
    """
    The list of Service endpoints to associate with the subnet. Possible values include: `Microsoft.AzureActiveDirectory`, `Microsoft.AzureCosmosDB`, `Microsoft.ContainerRegistry`, `Microsoft.EventHub`, `Microsoft.KeyVault`, `Microsoft.ServiceBus`, `Microsoft.Sql`, `Microsoft.Storage` and `Microsoft.Web`.
    """
    virtual_network_name: pulumi.Output[str]
    """
    The name of the virtual network to which to attach the subnet. Changing this forces a new resource to be created.
    """
    def __init__(__self__, resource_name, opts=None, address_prefix=None, address_prefixes=None, delegations=None, enforce_private_link_endpoint_network_policies=None, enforce_private_link_service_network_policies=None, name=None, resource_group_name=None, service_endpoints=None, virtual_network_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a subnet. Subnets represent network segments within the IP space defined by the virtual network.

        > **NOTE on Virtual Networks and Subnet's:** This provider currently
        provides both a standalone Subnet resource, and allows for Subnets to be defined in-line within the Virtual Network resource.
        At this time you cannot use a Virtual Network with in-line Subnets in conjunction with any Subnet resources. Doing so will cause a conflict of Subnet configurations and will overwrite Subnet's.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_prefix: The address prefix to use for the subnet.
        :param pulumi.Input[list] address_prefixes: The address prefixes to use for the subnet.
        :param pulumi.Input[list] delegations: One or more `delegation` blocks as defined below.
        :param pulumi.Input[bool] enforce_private_link_endpoint_network_policies: Enable or Disable network policies for the private link endpoint on the subnet. Default value is `false`. Conflicts with enforce_private_link_service_network_policies.
        :param pulumi.Input[bool] enforce_private_link_service_network_policies: Enable or Disable network policies for the private link service on the subnet. Default valule is `false`. Conflicts with `enforce_private_link_endpoint_network_policies`.
        :param pulumi.Input[str] name: The name of the subnet. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the subnet. Changing this forces a new resource to be created.
        :param pulumi.Input[list] service_endpoints: The list of Service endpoints to associate with the subnet. Possible values include: `Microsoft.AzureActiveDirectory`, `Microsoft.AzureCosmosDB`, `Microsoft.ContainerRegistry`, `Microsoft.EventHub`, `Microsoft.KeyVault`, `Microsoft.ServiceBus`, `Microsoft.Sql`, `Microsoft.Storage` and `Microsoft.Web`.
        :param pulumi.Input[str] virtual_network_name: The name of the virtual network to which to attach the subnet. Changing this forces a new resource to be created.

        The **delegations** object supports the following:

          * `name` (`pulumi.Input[str]`) - A name for this delegation.
          * `serviceDelegation` (`pulumi.Input[dict]`) - A `service_delegation` block as defined below.
            * `actions` (`pulumi.Input[list]`) - A list of Actions which should be delegated. This list is specific to the service to delegate to. Possible values include `Microsoft.Network/networkinterfaces/*`, `Microsoft.Network/virtualNetworks/subnets/action`, `Microsoft.Network/virtualNetworks/subnets/join/action`, `Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action` and `Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action`.
            * `name` (`pulumi.Input[str]`) - The name of service to delegate to. Possible values include `Microsoft.BareMetal/AzureVMware`, `Microsoft.BareMetal/CrayServers`, `Microsoft.Batch/batchAccounts`, `Microsoft.ContainerInstance/containerGroups`, `Microsoft.Databricks/workspaces`, `Microsoft.DBforPostgreSQL/serversv2`, `Microsoft.HardwareSecurityModules/dedicatedHSMs`, `Microsoft.Logic/integrationServiceEnvironments`, `Microsoft.Netapp/volumes`, `Microsoft.ServiceFabricMesh/networks`, `Microsoft.Sql/managedInstances`, `Microsoft.Sql/servers`, `Microsoft.StreamAnalytics/streamingJobs`, `Microsoft.Web/hostingEnvironments` and `Microsoft.Web/serverFarms`.
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

            __props__['address_prefix'] = address_prefix
            __props__['address_prefixes'] = address_prefixes
            __props__['delegations'] = delegations
            __props__['enforce_private_link_endpoint_network_policies'] = enforce_private_link_endpoint_network_policies
            __props__['enforce_private_link_service_network_policies'] = enforce_private_link_service_network_policies
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['service_endpoints'] = service_endpoints
            if virtual_network_name is None:
                raise TypeError("Missing required property 'virtual_network_name'")
            __props__['virtual_network_name'] = virtual_network_name
        super(Subnet, __self__).__init__(
            'azure:network/subnet:Subnet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, address_prefix=None, address_prefixes=None, delegations=None, enforce_private_link_endpoint_network_policies=None, enforce_private_link_service_network_policies=None, name=None, resource_group_name=None, service_endpoints=None, virtual_network_name=None):
        """
        Get an existing Subnet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_prefix: The address prefix to use for the subnet.
        :param pulumi.Input[list] address_prefixes: The address prefixes to use for the subnet.
        :param pulumi.Input[list] delegations: One or more `delegation` blocks as defined below.
        :param pulumi.Input[bool] enforce_private_link_endpoint_network_policies: Enable or Disable network policies for the private link endpoint on the subnet. Default value is `false`. Conflicts with enforce_private_link_service_network_policies.
        :param pulumi.Input[bool] enforce_private_link_service_network_policies: Enable or Disable network policies for the private link service on the subnet. Default valule is `false`. Conflicts with `enforce_private_link_endpoint_network_policies`.
        :param pulumi.Input[str] name: The name of the subnet. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the subnet. Changing this forces a new resource to be created.
        :param pulumi.Input[list] service_endpoints: The list of Service endpoints to associate with the subnet. Possible values include: `Microsoft.AzureActiveDirectory`, `Microsoft.AzureCosmosDB`, `Microsoft.ContainerRegistry`, `Microsoft.EventHub`, `Microsoft.KeyVault`, `Microsoft.ServiceBus`, `Microsoft.Sql`, `Microsoft.Storage` and `Microsoft.Web`.
        :param pulumi.Input[str] virtual_network_name: The name of the virtual network to which to attach the subnet. Changing this forces a new resource to be created.

        The **delegations** object supports the following:

          * `name` (`pulumi.Input[str]`) - A name for this delegation.
          * `serviceDelegation` (`pulumi.Input[dict]`) - A `service_delegation` block as defined below.
            * `actions` (`pulumi.Input[list]`) - A list of Actions which should be delegated. This list is specific to the service to delegate to. Possible values include `Microsoft.Network/networkinterfaces/*`, `Microsoft.Network/virtualNetworks/subnets/action`, `Microsoft.Network/virtualNetworks/subnets/join/action`, `Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action` and `Microsoft.Network/virtualNetworks/subnets/unprepareNetworkPolicies/action`.
            * `name` (`pulumi.Input[str]`) - The name of service to delegate to. Possible values include `Microsoft.BareMetal/AzureVMware`, `Microsoft.BareMetal/CrayServers`, `Microsoft.Batch/batchAccounts`, `Microsoft.ContainerInstance/containerGroups`, `Microsoft.Databricks/workspaces`, `Microsoft.DBforPostgreSQL/serversv2`, `Microsoft.HardwareSecurityModules/dedicatedHSMs`, `Microsoft.Logic/integrationServiceEnvironments`, `Microsoft.Netapp/volumes`, `Microsoft.ServiceFabricMesh/networks`, `Microsoft.Sql/managedInstances`, `Microsoft.Sql/servers`, `Microsoft.StreamAnalytics/streamingJobs`, `Microsoft.Web/hostingEnvironments` and `Microsoft.Web/serverFarms`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["address_prefix"] = address_prefix
        __props__["address_prefixes"] = address_prefixes
        __props__["delegations"] = delegations
        __props__["enforce_private_link_endpoint_network_policies"] = enforce_private_link_endpoint_network_policies
        __props__["enforce_private_link_service_network_policies"] = enforce_private_link_service_network_policies
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["service_endpoints"] = service_endpoints
        __props__["virtual_network_name"] = virtual_network_name
        return Subnet(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

