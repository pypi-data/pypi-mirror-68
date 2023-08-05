# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Frontdoor(pulumi.CustomResource):
    backend_pool_health_probes: pulumi.Output[list]
    """
    A `backend_pool_health_probe` block as defined below.

      * `enabled` (`bool`) - Is this health probe enabled? Dafaults to `true`.
      * `id` (`str`) - The ID of the FrontDoor.
      * `interval_in_seconds` (`float`) - The number of seconds between each Health Probe. Defaults to `120`.
      * `name` (`str`) - Specifies the name of the Health Probe.
      * `path` (`str`) - The path to use for the Health Probe. Default is `/`.
      * `probeMethod` (`str`) - Specifies HTTP method the health probe uses when querying the backend pool instances. Possible values include: `Get` and `Head`. Defaults to `Get`.
      * `protocol` (`str`) - Protocol scheme to use for the Health Probe. Defaults to `Http`.
    """
    backend_pool_load_balancings: pulumi.Output[list]
    """
    A `backend_pool_load_balancing` block as defined below.

      * `additionalLatencyMilliseconds` (`float`) - The additional latency in milliseconds for probes to fall into the lowest latency bucket. Defaults to `0`.
      * `id` (`str`) - The ID of the FrontDoor.
      * `name` (`str`) - Specifies the name of the Load Balancer.
      * `sampleSize` (`float`) - The number of samples to consider for load balancing decisions. Defaults to `4`.
      * `successfulSamplesRequired` (`float`) - The number of samples within the sample period that must succeed. Defaults to `2`.
    """
    backend_pools: pulumi.Output[list]
    """
    A `backend_pool` block as defined below.

      * `backends` (`list`) - A `backend` block as defined below.
        * `address` (`str`) - Location of the backend (IP address or FQDN)
        * `enabled` (`bool`) - Specifies if the backend is enabled or not. Valid options are `true` or `false`. Defaults to `true`.
        * `hostHeader` (`str`) - The value to use as the host header sent to the backend.
        * `httpPort` (`float`) - The HTTP TCP port number. Possible values are between `1` - `65535`.
        * `httpsPort` (`float`) - The HTTPS TCP port number. Possible values are between `1` - `65535`.
        * `priority` (`float`) - Priority to use for load balancing. Higher priorities will not be used for load balancing if any lower priority backend is healthy. Defaults to `1`.
        * `weight` (`float`) - Weight of this endpoint for load balancing purposes. Defaults to `50`.

      * `healthProbeName` (`str`) - Specifies the name of the `backend_pool_health_probe` block whithin this resource to use for this `Backend Pool`.
      * `id` (`str`) - The ID of the FrontDoor.
      * `loadBalancingName` (`str`) - Specifies the name of the `backend_pool_load_balancing` block within this resource to use for this `Backend Pool`.
      * `name` (`str`) - Specifies the name of the Backend Pool.
    """
    backend_pools_send_receive_timeout_seconds: pulumi.Output[float]
    """
    Specifies the send and receive timeout on forwarding request to the backend. When the timeout is reached, the request fails and returns. Possible values are between `0` - `240`. Defaults to `60`.
    """
    cname: pulumi.Output[str]
    """
    The host that each frontendEndpoint must CNAME to.
    """
    enforce_backend_pools_certificate_name_check: pulumi.Output[bool]
    """
    Enforce certificate name check on `HTTPS` requests to all backend pools, this setting will have no effect on `HTTP` requests. Permitted values are `true` or `false`.
    """
    friendly_name: pulumi.Output[str]
    """
    A friendly name for the Front Door service.
    """
    frontend_endpoints: pulumi.Output[list]
    """
    A `frontend_endpoint` block as defined below.

      * `customHttpsConfiguration` (`dict`) - A `custom_https_configuration` block as defined below.
        * `azureKeyVaultCertificateSecretName` (`str`) - The name of the Key Vault secret representing the full certificate PFX.
        * `azureKeyVaultCertificateSecretVersion` (`str`) - The version of the Key Vault secret representing the full certificate PFX.
        * `azureKeyVaultCertificateVaultId` (`str`) - The ID of the Key Vault containing the SSL certificate.
        * `certificateSource` (`str`) - Certificate source to encrypted `HTTPS` traffic with. Allowed values are `FrontDoor` or `AzureKeyVault`. Defaults to `FrontDoor`.
        * `minimum_tls_version` (`str`) - Minimum client TLS version supported.
        * `provisioningState` (`str`) - Provisioning state of the Front Door.
        * `provisioningSubstate` (`str`) - Provisioning substate of the Front Door

      * `customHttpsProvisioningEnabled` (`bool`) - Should the HTTPS protocol be enabled for a custom domain associated with the Front Door?
      * `host_name` (`str`) - Specifies the host name of the `frontend_endpoint`. Must be a domain name.
      * `id` (`str`) - The ID of the FrontDoor.
      * `name` (`str`) - Specifies the name of the `frontend_endpoint`.
      * `sessionAffinityEnabled` (`bool`) - Whether to allow session affinity on this host. Valid options are `true` or `false` Defaults to `false`.
      * `sessionAffinityTtlSeconds` (`float`) - The TTL to use in seconds for session affinity, if applicable. Defaults to `0`.
      * `webApplicationFirewallPolicyLinkId` (`str`) - Defines the Web Application Firewall policy `ID` for each host.
    """
    load_balancer_enabled: pulumi.Output[bool]
    """
    Should the Front Door Load Balancer be Enabled? Defaults to `true`.
    """
    location: pulumi.Output[str]
    name: pulumi.Output[str]
    """
    Specifies the name of the Front Door service. Changing this forces a new resource to be created.
    """
    resource_group_name: pulumi.Output[str]
    """
    Specifies the name of the Resource Group in which the Front Door service should exist. Changing this forces a new resource to be created.
    """
    routing_rules: pulumi.Output[list]
    """
    A `routing_rule` block as defined below.

      * `acceptedProtocols` (`list`) - Protocol schemes to match for the Backend Routing Rule. Defaults to `Http`.
      * `enabled` (`bool`) - `Enable` or `Disable` use of this Backend Routing Rule. Permitted values are `true` or `false`. Defaults to `true`.
      * `forwardingConfiguration` (`dict`) - A `forwarding_configuration` block as defined below.
        * `backendPoolName` (`str`) - Specifies the name of the Backend Pool to forward the incoming traffic to.
        * `cacheEnabled` (`bool`) - Specifies whether to Enable caching or not. Valid options are `true` or `false`. Defaults to `false`.
        * `cacheQueryParameterStripDirective` (`str`) - Defines cache behavior in releation to query string parameters. Valid options are `StripAll` or `StripNone`. Defaults to `StripAll`.
        * `cacheUseDynamicCompression` (`bool`) - Whether to use dynamic compression when caching. Valid options are `true` or `false`. Defaults to `false`.
        * `customForwardingPath` (`str`) - Path to use when constructing the request to forward to the backend. This functions as a URL Rewrite. Default behavior preserves the URL path.
        * `forwardingProtocol` (`str`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `HttpsOnly`.

      * `frontend_endpoints` (`list`) - The names of the `frontend_endpoint` blocks whithin this resource to associate with this `routing_rule`.
      * `id` (`str`) - The ID of the FrontDoor.
      * `name` (`str`) - Specifies the name of the Routing Rule.
      * `patternsToMatches` (`list`) - The route patterns for the Backend Routing Rule. Defaults to `/*`.
      * `redirectConfiguration` (`dict`) - A `redirect_configuration` block as defined below.
        * `customFragment` (`str`) - The destination fragment in the portion of URL after '#'. Set this to add a fragment to the redirect URL.
        * `customHost` (`str`) - Set this to change the URL for the redirection.
        * `customPath` (`str`) - The path to retain as per the incoming request, or update in the URL for the redirection.
        * `customQueryString` (`str`) - Replace any existing query string from the incoming request URL.
        * `redirectProtocol` (`str`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `MatchRequest`
        * `redirectType` (`str`) - Status code for the redirect. Valida options are `Moved`, `Found`, `TemporaryRedirect`, `PermanentRedirect`. Defaults to `Found`
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    def __init__(__self__, resource_name, opts=None, backend_pool_health_probes=None, backend_pool_load_balancings=None, backend_pools=None, backend_pools_send_receive_timeout_seconds=None, enforce_backend_pools_certificate_name_check=None, friendly_name=None, frontend_endpoints=None, load_balancer_enabled=None, location=None, name=None, resource_group_name=None, routing_rules=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an Azure Front Door instance.

        Azure Front Door Service is Microsoft's highly available and scalable web application acceleration platform and global HTTP(s) load balancer. It provides built-in DDoS protection and application layer security and caching. Front Door enables you to build applications that maximize and automate high-availability and performance for your end-users. Use Front Door with Azure services including Web/Mobile Apps, Cloud Services and Virtual Machines – or combine it with on-premises services for hybrid deployments and smooth cloud migration.

        Below are some of the key scenarios that Azure Front Door Service addresses:
        * Use Front Door to improve application scale and availability with instant multi-region failover
        * Use Front Door to improve application performance with SSL offload and routing requests to the fastest available application backend.
        * Use Front Door for application layer security and DDoS protection for your application.



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] backend_pool_health_probes: A `backend_pool_health_probe` block as defined below.
        :param pulumi.Input[list] backend_pool_load_balancings: A `backend_pool_load_balancing` block as defined below.
        :param pulumi.Input[list] backend_pools: A `backend_pool` block as defined below.
        :param pulumi.Input[float] backend_pools_send_receive_timeout_seconds: Specifies the send and receive timeout on forwarding request to the backend. When the timeout is reached, the request fails and returns. Possible values are between `0` - `240`. Defaults to `60`.
        :param pulumi.Input[bool] enforce_backend_pools_certificate_name_check: Enforce certificate name check on `HTTPS` requests to all backend pools, this setting will have no effect on `HTTP` requests. Permitted values are `true` or `false`.
        :param pulumi.Input[str] friendly_name: A friendly name for the Front Door service.
        :param pulumi.Input[list] frontend_endpoints: A `frontend_endpoint` block as defined below.
        :param pulumi.Input[bool] load_balancer_enabled: Should the Front Door Load Balancer be Enabled? Defaults to `true`.
        :param pulumi.Input[str] name: Specifies the name of the Front Door service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Front Door service should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[list] routing_rules: A `routing_rule` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **backend_pool_health_probes** object supports the following:

          * `enabled` (`pulumi.Input[bool]`) - Is this health probe enabled? Dafaults to `true`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `interval_in_seconds` (`pulumi.Input[float]`) - The number of seconds between each Health Probe. Defaults to `120`.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Health Probe.
          * `path` (`pulumi.Input[str]`) - The path to use for the Health Probe. Default is `/`.
          * `probeMethod` (`pulumi.Input[str]`) - Specifies HTTP method the health probe uses when querying the backend pool instances. Possible values include: `Get` and `Head`. Defaults to `Get`.
          * `protocol` (`pulumi.Input[str]`) - Protocol scheme to use for the Health Probe. Defaults to `Http`.

        The **backend_pool_load_balancings** object supports the following:

          * `additionalLatencyMilliseconds` (`pulumi.Input[float]`) - The additional latency in milliseconds for probes to fall into the lowest latency bucket. Defaults to `0`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Load Balancer.
          * `sampleSize` (`pulumi.Input[float]`) - The number of samples to consider for load balancing decisions. Defaults to `4`.
          * `successfulSamplesRequired` (`pulumi.Input[float]`) - The number of samples within the sample period that must succeed. Defaults to `2`.

        The **backend_pools** object supports the following:

          * `backends` (`pulumi.Input[list]`) - A `backend` block as defined below.
            * `address` (`pulumi.Input[str]`) - Location of the backend (IP address or FQDN)
            * `enabled` (`pulumi.Input[bool]`) - Specifies if the backend is enabled or not. Valid options are `true` or `false`. Defaults to `true`.
            * `hostHeader` (`pulumi.Input[str]`) - The value to use as the host header sent to the backend.
            * `httpPort` (`pulumi.Input[float]`) - The HTTP TCP port number. Possible values are between `1` - `65535`.
            * `httpsPort` (`pulumi.Input[float]`) - The HTTPS TCP port number. Possible values are between `1` - `65535`.
            * `priority` (`pulumi.Input[float]`) - Priority to use for load balancing. Higher priorities will not be used for load balancing if any lower priority backend is healthy. Defaults to `1`.
            * `weight` (`pulumi.Input[float]`) - Weight of this endpoint for load balancing purposes. Defaults to `50`.

          * `healthProbeName` (`pulumi.Input[str]`) - Specifies the name of the `backend_pool_health_probe` block whithin this resource to use for this `Backend Pool`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `loadBalancingName` (`pulumi.Input[str]`) - Specifies the name of the `backend_pool_load_balancing` block within this resource to use for this `Backend Pool`.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Backend Pool.

        The **frontend_endpoints** object supports the following:

          * `customHttpsConfiguration` (`pulumi.Input[dict]`) - A `custom_https_configuration` block as defined below.
            * `azureKeyVaultCertificateSecretName` (`pulumi.Input[str]`) - The name of the Key Vault secret representing the full certificate PFX.
            * `azureKeyVaultCertificateSecretVersion` (`pulumi.Input[str]`) - The version of the Key Vault secret representing the full certificate PFX.
            * `azureKeyVaultCertificateVaultId` (`pulumi.Input[str]`) - The ID of the Key Vault containing the SSL certificate.
            * `certificateSource` (`pulumi.Input[str]`) - Certificate source to encrypted `HTTPS` traffic with. Allowed values are `FrontDoor` or `AzureKeyVault`. Defaults to `FrontDoor`.
            * `minimum_tls_version` (`pulumi.Input[str]`) - Minimum client TLS version supported.
            * `provisioningState` (`pulumi.Input[str]`) - Provisioning state of the Front Door.
            * `provisioningSubstate` (`pulumi.Input[str]`) - Provisioning substate of the Front Door

          * `customHttpsProvisioningEnabled` (`pulumi.Input[bool]`) - Should the HTTPS protocol be enabled for a custom domain associated with the Front Door?
          * `host_name` (`pulumi.Input[str]`) - Specifies the host name of the `frontend_endpoint`. Must be a domain name.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the `frontend_endpoint`.
          * `sessionAffinityEnabled` (`pulumi.Input[bool]`) - Whether to allow session affinity on this host. Valid options are `true` or `false` Defaults to `false`.
          * `sessionAffinityTtlSeconds` (`pulumi.Input[float]`) - The TTL to use in seconds for session affinity, if applicable. Defaults to `0`.
          * `webApplicationFirewallPolicyLinkId` (`pulumi.Input[str]`) - Defines the Web Application Firewall policy `ID` for each host.

        The **routing_rules** object supports the following:

          * `acceptedProtocols` (`pulumi.Input[list]`) - Protocol schemes to match for the Backend Routing Rule. Defaults to `Http`.
          * `enabled` (`pulumi.Input[bool]`) - `Enable` or `Disable` use of this Backend Routing Rule. Permitted values are `true` or `false`. Defaults to `true`.
          * `forwardingConfiguration` (`pulumi.Input[dict]`) - A `forwarding_configuration` block as defined below.
            * `backendPoolName` (`pulumi.Input[str]`) - Specifies the name of the Backend Pool to forward the incoming traffic to.
            * `cacheEnabled` (`pulumi.Input[bool]`) - Specifies whether to Enable caching or not. Valid options are `true` or `false`. Defaults to `false`.
            * `cacheQueryParameterStripDirective` (`pulumi.Input[str]`) - Defines cache behavior in releation to query string parameters. Valid options are `StripAll` or `StripNone`. Defaults to `StripAll`.
            * `cacheUseDynamicCompression` (`pulumi.Input[bool]`) - Whether to use dynamic compression when caching. Valid options are `true` or `false`. Defaults to `false`.
            * `customForwardingPath` (`pulumi.Input[str]`) - Path to use when constructing the request to forward to the backend. This functions as a URL Rewrite. Default behavior preserves the URL path.
            * `forwardingProtocol` (`pulumi.Input[str]`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `HttpsOnly`.

          * `frontend_endpoints` (`pulumi.Input[list]`) - The names of the `frontend_endpoint` blocks whithin this resource to associate with this `routing_rule`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Routing Rule.
          * `patternsToMatches` (`pulumi.Input[list]`) - The route patterns for the Backend Routing Rule. Defaults to `/*`.
          * `redirectConfiguration` (`pulumi.Input[dict]`) - A `redirect_configuration` block as defined below.
            * `customFragment` (`pulumi.Input[str]`) - The destination fragment in the portion of URL after '#'. Set this to add a fragment to the redirect URL.
            * `customHost` (`pulumi.Input[str]`) - Set this to change the URL for the redirection.
            * `customPath` (`pulumi.Input[str]`) - The path to retain as per the incoming request, or update in the URL for the redirection.
            * `customQueryString` (`pulumi.Input[str]`) - Replace any existing query string from the incoming request URL.
            * `redirectProtocol` (`pulumi.Input[str]`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `MatchRequest`
            * `redirectType` (`pulumi.Input[str]`) - Status code for the redirect. Valida options are `Moved`, `Found`, `TemporaryRedirect`, `PermanentRedirect`. Defaults to `Found`
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

            if backend_pool_health_probes is None:
                raise TypeError("Missing required property 'backend_pool_health_probes'")
            __props__['backend_pool_health_probes'] = backend_pool_health_probes
            if backend_pool_load_balancings is None:
                raise TypeError("Missing required property 'backend_pool_load_balancings'")
            __props__['backend_pool_load_balancings'] = backend_pool_load_balancings
            if backend_pools is None:
                raise TypeError("Missing required property 'backend_pools'")
            __props__['backend_pools'] = backend_pools
            __props__['backend_pools_send_receive_timeout_seconds'] = backend_pools_send_receive_timeout_seconds
            if enforce_backend_pools_certificate_name_check is None:
                raise TypeError("Missing required property 'enforce_backend_pools_certificate_name_check'")
            __props__['enforce_backend_pools_certificate_name_check'] = enforce_backend_pools_certificate_name_check
            __props__['friendly_name'] = friendly_name
            if frontend_endpoints is None:
                raise TypeError("Missing required property 'frontend_endpoints'")
            __props__['frontend_endpoints'] = frontend_endpoints
            __props__['load_balancer_enabled'] = load_balancer_enabled
            __props__['location'] = location
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if routing_rules is None:
                raise TypeError("Missing required property 'routing_rules'")
            __props__['routing_rules'] = routing_rules
            __props__['tags'] = tags
            __props__['cname'] = None
        super(Frontdoor, __self__).__init__(
            'azure:frontdoor/frontdoor:Frontdoor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, backend_pool_health_probes=None, backend_pool_load_balancings=None, backend_pools=None, backend_pools_send_receive_timeout_seconds=None, cname=None, enforce_backend_pools_certificate_name_check=None, friendly_name=None, frontend_endpoints=None, load_balancer_enabled=None, location=None, name=None, resource_group_name=None, routing_rules=None, tags=None):
        """
        Get an existing Frontdoor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] backend_pool_health_probes: A `backend_pool_health_probe` block as defined below.
        :param pulumi.Input[list] backend_pool_load_balancings: A `backend_pool_load_balancing` block as defined below.
        :param pulumi.Input[list] backend_pools: A `backend_pool` block as defined below.
        :param pulumi.Input[float] backend_pools_send_receive_timeout_seconds: Specifies the send and receive timeout on forwarding request to the backend. When the timeout is reached, the request fails and returns. Possible values are between `0` - `240`. Defaults to `60`.
        :param pulumi.Input[str] cname: The host that each frontendEndpoint must CNAME to.
        :param pulumi.Input[bool] enforce_backend_pools_certificate_name_check: Enforce certificate name check on `HTTPS` requests to all backend pools, this setting will have no effect on `HTTP` requests. Permitted values are `true` or `false`.
        :param pulumi.Input[str] friendly_name: A friendly name for the Front Door service.
        :param pulumi.Input[list] frontend_endpoints: A `frontend_endpoint` block as defined below.
        :param pulumi.Input[bool] load_balancer_enabled: Should the Front Door Load Balancer be Enabled? Defaults to `true`.
        :param pulumi.Input[str] name: Specifies the name of the Front Door service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: Specifies the name of the Resource Group in which the Front Door service should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[list] routing_rules: A `routing_rule` block as defined below.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.

        The **backend_pool_health_probes** object supports the following:

          * `enabled` (`pulumi.Input[bool]`) - Is this health probe enabled? Dafaults to `true`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `interval_in_seconds` (`pulumi.Input[float]`) - The number of seconds between each Health Probe. Defaults to `120`.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Health Probe.
          * `path` (`pulumi.Input[str]`) - The path to use for the Health Probe. Default is `/`.
          * `probeMethod` (`pulumi.Input[str]`) - Specifies HTTP method the health probe uses when querying the backend pool instances. Possible values include: `Get` and `Head`. Defaults to `Get`.
          * `protocol` (`pulumi.Input[str]`) - Protocol scheme to use for the Health Probe. Defaults to `Http`.

        The **backend_pool_load_balancings** object supports the following:

          * `additionalLatencyMilliseconds` (`pulumi.Input[float]`) - The additional latency in milliseconds for probes to fall into the lowest latency bucket. Defaults to `0`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Load Balancer.
          * `sampleSize` (`pulumi.Input[float]`) - The number of samples to consider for load balancing decisions. Defaults to `4`.
          * `successfulSamplesRequired` (`pulumi.Input[float]`) - The number of samples within the sample period that must succeed. Defaults to `2`.

        The **backend_pools** object supports the following:

          * `backends` (`pulumi.Input[list]`) - A `backend` block as defined below.
            * `address` (`pulumi.Input[str]`) - Location of the backend (IP address or FQDN)
            * `enabled` (`pulumi.Input[bool]`) - Specifies if the backend is enabled or not. Valid options are `true` or `false`. Defaults to `true`.
            * `hostHeader` (`pulumi.Input[str]`) - The value to use as the host header sent to the backend.
            * `httpPort` (`pulumi.Input[float]`) - The HTTP TCP port number. Possible values are between `1` - `65535`.
            * `httpsPort` (`pulumi.Input[float]`) - The HTTPS TCP port number. Possible values are between `1` - `65535`.
            * `priority` (`pulumi.Input[float]`) - Priority to use for load balancing. Higher priorities will not be used for load balancing if any lower priority backend is healthy. Defaults to `1`.
            * `weight` (`pulumi.Input[float]`) - Weight of this endpoint for load balancing purposes. Defaults to `50`.

          * `healthProbeName` (`pulumi.Input[str]`) - Specifies the name of the `backend_pool_health_probe` block whithin this resource to use for this `Backend Pool`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `loadBalancingName` (`pulumi.Input[str]`) - Specifies the name of the `backend_pool_load_balancing` block within this resource to use for this `Backend Pool`.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Backend Pool.

        The **frontend_endpoints** object supports the following:

          * `customHttpsConfiguration` (`pulumi.Input[dict]`) - A `custom_https_configuration` block as defined below.
            * `azureKeyVaultCertificateSecretName` (`pulumi.Input[str]`) - The name of the Key Vault secret representing the full certificate PFX.
            * `azureKeyVaultCertificateSecretVersion` (`pulumi.Input[str]`) - The version of the Key Vault secret representing the full certificate PFX.
            * `azureKeyVaultCertificateVaultId` (`pulumi.Input[str]`) - The ID of the Key Vault containing the SSL certificate.
            * `certificateSource` (`pulumi.Input[str]`) - Certificate source to encrypted `HTTPS` traffic with. Allowed values are `FrontDoor` or `AzureKeyVault`. Defaults to `FrontDoor`.
            * `minimum_tls_version` (`pulumi.Input[str]`) - Minimum client TLS version supported.
            * `provisioningState` (`pulumi.Input[str]`) - Provisioning state of the Front Door.
            * `provisioningSubstate` (`pulumi.Input[str]`) - Provisioning substate of the Front Door

          * `customHttpsProvisioningEnabled` (`pulumi.Input[bool]`) - Should the HTTPS protocol be enabled for a custom domain associated with the Front Door?
          * `host_name` (`pulumi.Input[str]`) - Specifies the host name of the `frontend_endpoint`. Must be a domain name.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the `frontend_endpoint`.
          * `sessionAffinityEnabled` (`pulumi.Input[bool]`) - Whether to allow session affinity on this host. Valid options are `true` or `false` Defaults to `false`.
          * `sessionAffinityTtlSeconds` (`pulumi.Input[float]`) - The TTL to use in seconds for session affinity, if applicable. Defaults to `0`.
          * `webApplicationFirewallPolicyLinkId` (`pulumi.Input[str]`) - Defines the Web Application Firewall policy `ID` for each host.

        The **routing_rules** object supports the following:

          * `acceptedProtocols` (`pulumi.Input[list]`) - Protocol schemes to match for the Backend Routing Rule. Defaults to `Http`.
          * `enabled` (`pulumi.Input[bool]`) - `Enable` or `Disable` use of this Backend Routing Rule. Permitted values are `true` or `false`. Defaults to `true`.
          * `forwardingConfiguration` (`pulumi.Input[dict]`) - A `forwarding_configuration` block as defined below.
            * `backendPoolName` (`pulumi.Input[str]`) - Specifies the name of the Backend Pool to forward the incoming traffic to.
            * `cacheEnabled` (`pulumi.Input[bool]`) - Specifies whether to Enable caching or not. Valid options are `true` or `false`. Defaults to `false`.
            * `cacheQueryParameterStripDirective` (`pulumi.Input[str]`) - Defines cache behavior in releation to query string parameters. Valid options are `StripAll` or `StripNone`. Defaults to `StripAll`.
            * `cacheUseDynamicCompression` (`pulumi.Input[bool]`) - Whether to use dynamic compression when caching. Valid options are `true` or `false`. Defaults to `false`.
            * `customForwardingPath` (`pulumi.Input[str]`) - Path to use when constructing the request to forward to the backend. This functions as a URL Rewrite. Default behavior preserves the URL path.
            * `forwardingProtocol` (`pulumi.Input[str]`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `HttpsOnly`.

          * `frontend_endpoints` (`pulumi.Input[list]`) - The names of the `frontend_endpoint` blocks whithin this resource to associate with this `routing_rule`.
          * `id` (`pulumi.Input[str]`) - The ID of the FrontDoor.
          * `name` (`pulumi.Input[str]`) - Specifies the name of the Routing Rule.
          * `patternsToMatches` (`pulumi.Input[list]`) - The route patterns for the Backend Routing Rule. Defaults to `/*`.
          * `redirectConfiguration` (`pulumi.Input[dict]`) - A `redirect_configuration` block as defined below.
            * `customFragment` (`pulumi.Input[str]`) - The destination fragment in the portion of URL after '#'. Set this to add a fragment to the redirect URL.
            * `customHost` (`pulumi.Input[str]`) - Set this to change the URL for the redirection.
            * `customPath` (`pulumi.Input[str]`) - The path to retain as per the incoming request, or update in the URL for the redirection.
            * `customQueryString` (`pulumi.Input[str]`) - Replace any existing query string from the incoming request URL.
            * `redirectProtocol` (`pulumi.Input[str]`) - Protocol to use when redirecting. Valid options are `HttpOnly`, `HttpsOnly`, or `MatchRequest`. Defaults to `MatchRequest`
            * `redirectType` (`pulumi.Input[str]`) - Status code for the redirect. Valida options are `Moved`, `Found`, `TemporaryRedirect`, `PermanentRedirect`. Defaults to `Found`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["backend_pool_health_probes"] = backend_pool_health_probes
        __props__["backend_pool_load_balancings"] = backend_pool_load_balancings
        __props__["backend_pools"] = backend_pools
        __props__["backend_pools_send_receive_timeout_seconds"] = backend_pools_send_receive_timeout_seconds
        __props__["cname"] = cname
        __props__["enforce_backend_pools_certificate_name_check"] = enforce_backend_pools_certificate_name_check
        __props__["friendly_name"] = friendly_name
        __props__["frontend_endpoints"] = frontend_endpoints
        __props__["load_balancer_enabled"] = load_balancer_enabled
        __props__["location"] = location
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["routing_rules"] = routing_rules
        __props__["tags"] = tags
        return Frontdoor(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

