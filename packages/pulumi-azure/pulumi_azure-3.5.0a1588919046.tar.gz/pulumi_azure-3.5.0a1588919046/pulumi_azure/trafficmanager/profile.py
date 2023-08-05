# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

warnings.warn("azure.trafficmanager.Profile has been deprecated in favour of azure.network.TrafficManagerProfile", DeprecationWarning)
class Profile(pulumi.CustomResource):
    dns_config: pulumi.Output[dict]
    """
    This block specifies the DNS configuration of the Profile, it supports the fields documented below.

      * `relativeName` (`str`) - The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
      * `ttl` (`float`) - The TTL value of the Profile used by Local DNS resolvers and clients.
    """
    fqdn: pulumi.Output[str]
    """
    The FQDN of the created Profile.
    """
    monitor_config: pulumi.Output[dict]
    """
    This block specifies the Endpoint monitoring configuration for the Profile, it supports the fields documented below.

      * `custom_headers` (`list`) - One or more `custom_header` blocks as defined below.
        * `name` (`str`) - The name of the custom header.
        * `value` (`str`) - The value of custom header. Applicable for Http and Https protocol.

      * `expectedStatusCodeRanges` (`list`) - A list of status code ranges in the format of `100-101`.
      * `interval_in_seconds` (`float`) - The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
      * `path` (`str`) - The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
      * `port` (`float`) - The port number used by the monitoring checks.
      * `protocol` (`str`) - The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
      * `timeoutInSeconds` (`float`) - The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
      * `toleratedNumberOfFailures` (`float`) - The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
    """
    name: pulumi.Output[str]
    """
    The name of the Traffic Manager profile. Changing this forces a new resource to be created.
    """
    profile_status: pulumi.Output[str]
    """
    The status of the profile, can be set to either `Enabled` or `Disabled`. Defaults to `Enabled`.
    """
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Traffic Manager profile.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    traffic_routing_method: pulumi.Output[str]
    """
    Specifies the algorithm used to route traffic, possible values are:
    """
    warnings.warn("azure.trafficmanager.Profile has been deprecated in favour of azure.network.TrafficManagerProfile", DeprecationWarning)
    def __init__(__self__, resource_name, opts=None, dns_config=None, monitor_config=None, name=None, profile_status=None, resource_group_name=None, tags=None, traffic_routing_method=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Traffic Manager Profile to which multiple endpoints can be attached.



        Deprecated: azure.trafficmanager.Profile has been deprecated in favour of azure.network.TrafficManagerProfile

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] dns_config: This block specifies the DNS configuration of the Profile, it supports the fields documented below.
        :param pulumi.Input[dict] monitor_config: This block specifies the Endpoint monitoring configuration for the Profile, it supports the fields documented below.
        :param pulumi.Input[str] name: The name of the Traffic Manager profile. Changing this forces a new resource to be created.
        :param pulumi.Input[str] profile_status: The status of the profile, can be set to either `Enabled` or `Disabled`. Defaults to `Enabled`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Traffic Manager profile.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] traffic_routing_method: Specifies the algorithm used to route traffic, possible values are:

        The **dns_config** object supports the following:

          * `relativeName` (`pulumi.Input[str]`) - The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
          * `ttl` (`pulumi.Input[float]`) - The TTL value of the Profile used by Local DNS resolvers and clients.

        The **monitor_config** object supports the following:

          * `custom_headers` (`pulumi.Input[list]`) - One or more `custom_header` blocks as defined below.
            * `name` (`pulumi.Input[str]`) - The name of the custom header.
            * `value` (`pulumi.Input[str]`) - The value of custom header. Applicable for Http and Https protocol.

          * `expectedStatusCodeRanges` (`pulumi.Input[list]`) - A list of status code ranges in the format of `100-101`.
          * `interval_in_seconds` (`pulumi.Input[float]`) - The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
          * `path` (`pulumi.Input[str]`) - The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
          * `port` (`pulumi.Input[float]`) - The port number used by the monitoring checks.
          * `protocol` (`pulumi.Input[str]`) - The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
          * `timeoutInSeconds` (`pulumi.Input[float]`) - The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
          * `toleratedNumberOfFailures` (`pulumi.Input[float]`) - The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
        """
        pulumi.log.warn("Profile is deprecated: azure.trafficmanager.Profile has been deprecated in favour of azure.network.TrafficManagerProfile")
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

            if dns_config is None:
                raise TypeError("Missing required property 'dns_config'")
            __props__['dns_config'] = dns_config
            if monitor_config is None:
                raise TypeError("Missing required property 'monitor_config'")
            __props__['monitor_config'] = monitor_config
            __props__['name'] = name
            __props__['profile_status'] = profile_status
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            if traffic_routing_method is None:
                raise TypeError("Missing required property 'traffic_routing_method'")
            __props__['traffic_routing_method'] = traffic_routing_method
            __props__['fqdn'] = None
        super(Profile, __self__).__init__(
            'azure:trafficmanager/profile:Profile',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, dns_config=None, fqdn=None, monitor_config=None, name=None, profile_status=None, resource_group_name=None, tags=None, traffic_routing_method=None):
        """
        Get an existing Profile resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[dict] dns_config: This block specifies the DNS configuration of the Profile, it supports the fields documented below.
        :param pulumi.Input[str] fqdn: The FQDN of the created Profile.
        :param pulumi.Input[dict] monitor_config: This block specifies the Endpoint monitoring configuration for the Profile, it supports the fields documented below.
        :param pulumi.Input[str] name: The name of the Traffic Manager profile. Changing this forces a new resource to be created.
        :param pulumi.Input[str] profile_status: The status of the profile, can be set to either `Enabled` or `Disabled`. Defaults to `Enabled`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Traffic Manager profile.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] traffic_routing_method: Specifies the algorithm used to route traffic, possible values are:

        The **dns_config** object supports the following:

          * `relativeName` (`pulumi.Input[str]`) - The relative domain name, this is combined with the domain name used by Traffic Manager to form the FQDN which is exported as documented below. Changing this forces a new resource to be created.
          * `ttl` (`pulumi.Input[float]`) - The TTL value of the Profile used by Local DNS resolvers and clients.

        The **monitor_config** object supports the following:

          * `custom_headers` (`pulumi.Input[list]`) - One or more `custom_header` blocks as defined below.
            * `name` (`pulumi.Input[str]`) - The name of the custom header.
            * `value` (`pulumi.Input[str]`) - The value of custom header. Applicable for Http and Https protocol.

          * `expectedStatusCodeRanges` (`pulumi.Input[list]`) - A list of status code ranges in the format of `100-101`.
          * `interval_in_seconds` (`pulumi.Input[float]`) - The interval used to check the endpoint health from a Traffic Manager probing agent. You can specify two values here: `30` (normal probing) and `10` (fast probing). The default value is `30`.
          * `path` (`pulumi.Input[str]`) - The path used by the monitoring checks. Required when `protocol` is set to `HTTP` or `HTTPS` - cannot be set when `protocol` is set to `TCP`.
          * `port` (`pulumi.Input[float]`) - The port number used by the monitoring checks.
          * `protocol` (`pulumi.Input[str]`) - The protocol used by the monitoring checks, supported values are `HTTP`, `HTTPS` and `TCP`.
          * `timeoutInSeconds` (`pulumi.Input[float]`) - The amount of time the Traffic Manager probing agent should wait before considering that check a failure when a health check probe is sent to the endpoint. If `interval_in_seconds` is set to `30`, then `timeout_in_seconds` can be between `5` and `10`. The default value is `10`. If `interval_in_seconds` is set to `10`, then valid values are between `5` and `9` and `timeout_in_seconds` is required.
          * `toleratedNumberOfFailures` (`pulumi.Input[float]`) - The number of failures a Traffic Manager probing agent tolerates before marking that endpoint as unhealthy. Valid values are between `0` and `9`. The default value is `3`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["dns_config"] = dns_config
        __props__["fqdn"] = fqdn
        __props__["monitor_config"] = monitor_config
        __props__["name"] = name
        __props__["profile_status"] = profile_status
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        __props__["traffic_routing_method"] = traffic_routing_method
        return Profile(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

