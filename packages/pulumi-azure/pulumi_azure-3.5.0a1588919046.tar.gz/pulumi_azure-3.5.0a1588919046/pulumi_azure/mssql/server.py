# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Server(pulumi.CustomResource):
    administrator_login: pulumi.Output[str]
    """
    The administrator login name for the new server. Changing this forces a new resource to be created.
    """
    administrator_login_password: pulumi.Output[str]
    """
    The password associated with the `administrator_login` user. Needs to comply with Azure's [Password Policy](https://msdn.microsoft.com/library/ms161959.aspx)
    """
    connection_policy: pulumi.Output[str]
    """
    The connection policy the server will use. Possible values are `Default`, `Proxy`, and `Redirect`. Defaults to `Default`.
    """
    extended_auditing_policy: pulumi.Output[dict]
    """
    A `extended_auditing_policy` block as defined below.

      * `retention_in_days` (`float`) - (Optional) Specifies the number of days to retain logs for in the storage account.
      * `storage_account_access_key` (`str`) - (Required)  Specifies the access key to use for the auditing storage account.
      * `storageAccountAccessKeyIsSecondary` (`bool`) - (Optional) Specifies whether `storage_account_access_key` value is the storage's secondary key.
      * `storage_endpoint` (`str`) - (Required) Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net).
    """
    fully_qualified_domain_name: pulumi.Output[str]
    """
    The fully qualified domain name of the Azure SQL Server (e.g. myServerName.database.windows.net)
    """
    identity: pulumi.Output[dict]
    """
    An `identity` block as defined below.

      * `principal_id` (`str`) - The Principal ID for the Service Principal associated with the Identity of this SQL Server.
      * `tenant_id` (`str`) - The Tenant ID for the Service Principal associated with the Identity of this SQL Server.
      * `type` (`str`) - Specifies the identity type of the Microsoft SQL Server. At this time the only allowed value is `SystemAssigned`.
    """
    location: pulumi.Output[str]
    """
    Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
    """
    name: pulumi.Output[str]
    """
    The name of the Microsoft SQL Server. This needs to be globally unique within Azure.
    """
    public_network_access_enabled: pulumi.Output[bool]
    resource_group_name: pulumi.Output[str]
    """
    The name of the resource group in which to create the Microsoft SQL Server.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    version: pulumi.Output[str]
    """
    The version for the new server. Valid values are: 2.0 (for v11 server) and 12.0 (for v12 server).
    """
    def __init__(__self__, resource_name, opts=None, administrator_login=None, administrator_login_password=None, connection_policy=None, extended_auditing_policy=None, identity=None, location=None, name=None, public_network_access_enabled=None, resource_group_name=None, tags=None, version=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages a Microsoft SQL Azure Database Server.

        > **Note:** All arguments including the administrator login and password will be stored in the raw state as plain-text.
        [Read more about sensitive data in state](https://www.terraform.io/docs/state/sensitive-data.html).



        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_login: The administrator login name for the new server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] administrator_login_password: The password associated with the `administrator_login` user. Needs to comply with Azure's [Password Policy](https://msdn.microsoft.com/library/ms161959.aspx)
        :param pulumi.Input[str] connection_policy: The connection policy the server will use. Possible values are `Default`, `Proxy`, and `Redirect`. Defaults to `Default`.
        :param pulumi.Input[dict] extended_auditing_policy: A `extended_auditing_policy` block as defined below.
        :param pulumi.Input[dict] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Microsoft SQL Server. This needs to be globally unique within Azure.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Microsoft SQL Server.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] version: The version for the new server. Valid values are: 2.0 (for v11 server) and 12.0 (for v12 server).

        The **extended_auditing_policy** object supports the following:

          * `retention_in_days` (`pulumi.Input[float]`) - (Optional) Specifies the number of days to retain logs for in the storage account.
          * `storage_account_access_key` (`pulumi.Input[str]`) - (Required)  Specifies the access key to use for the auditing storage account.
          * `storageAccountAccessKeyIsSecondary` (`pulumi.Input[bool]`) - (Optional) Specifies whether `storage_account_access_key` value is the storage's secondary key.
          * `storage_endpoint` (`pulumi.Input[str]`) - (Required) Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net).

        The **identity** object supports the following:

          * `principal_id` (`pulumi.Input[str]`) - The Principal ID for the Service Principal associated with the Identity of this SQL Server.
          * `tenant_id` (`pulumi.Input[str]`) - The Tenant ID for the Service Principal associated with the Identity of this SQL Server.
          * `type` (`pulumi.Input[str]`) - Specifies the identity type of the Microsoft SQL Server. At this time the only allowed value is `SystemAssigned`.
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

            if administrator_login is None:
                raise TypeError("Missing required property 'administrator_login'")
            __props__['administrator_login'] = administrator_login
            if administrator_login_password is None:
                raise TypeError("Missing required property 'administrator_login_password'")
            __props__['administrator_login_password'] = administrator_login_password
            __props__['connection_policy'] = connection_policy
            __props__['extended_auditing_policy'] = extended_auditing_policy
            __props__['identity'] = identity
            __props__['location'] = location
            __props__['name'] = name
            __props__['public_network_access_enabled'] = public_network_access_enabled
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            if version is None:
                raise TypeError("Missing required property 'version'")
            __props__['version'] = version
            __props__['fully_qualified_domain_name'] = None
        super(Server, __self__).__init__(
            'azure:mssql/server:Server',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, administrator_login=None, administrator_login_password=None, connection_policy=None, extended_auditing_policy=None, fully_qualified_domain_name=None, identity=None, location=None, name=None, public_network_access_enabled=None, resource_group_name=None, tags=None, version=None):
        """
        Get an existing Server resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_login: The administrator login name for the new server. Changing this forces a new resource to be created.
        :param pulumi.Input[str] administrator_login_password: The password associated with the `administrator_login` user. Needs to comply with Azure's [Password Policy](https://msdn.microsoft.com/library/ms161959.aspx)
        :param pulumi.Input[str] connection_policy: The connection policy the server will use. Possible values are `Default`, `Proxy`, and `Redirect`. Defaults to `Default`.
        :param pulumi.Input[dict] extended_auditing_policy: A `extended_auditing_policy` block as defined below.
        :param pulumi.Input[str] fully_qualified_domain_name: The fully qualified domain name of the Azure SQL Server (e.g. myServerName.database.windows.net)
        :param pulumi.Input[dict] identity: An `identity` block as defined below.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: The name of the Microsoft SQL Server. This needs to be globally unique within Azure.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the Microsoft SQL Server.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] version: The version for the new server. Valid values are: 2.0 (for v11 server) and 12.0 (for v12 server).

        The **extended_auditing_policy** object supports the following:

          * `retention_in_days` (`pulumi.Input[float]`) - (Optional) Specifies the number of days to retain logs for in the storage account.
          * `storage_account_access_key` (`pulumi.Input[str]`) - (Required)  Specifies the access key to use for the auditing storage account.
          * `storageAccountAccessKeyIsSecondary` (`pulumi.Input[bool]`) - (Optional) Specifies whether `storage_account_access_key` value is the storage's secondary key.
          * `storage_endpoint` (`pulumi.Input[str]`) - (Required) Specifies the blob storage endpoint (e.g. https://MyAccount.blob.core.windows.net).

        The **identity** object supports the following:

          * `principal_id` (`pulumi.Input[str]`) - The Principal ID for the Service Principal associated with the Identity of this SQL Server.
          * `tenant_id` (`pulumi.Input[str]`) - The Tenant ID for the Service Principal associated with the Identity of this SQL Server.
          * `type` (`pulumi.Input[str]`) - Specifies the identity type of the Microsoft SQL Server. At this time the only allowed value is `SystemAssigned`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["administrator_login"] = administrator_login
        __props__["administrator_login_password"] = administrator_login_password
        __props__["connection_policy"] = connection_policy
        __props__["extended_auditing_policy"] = extended_auditing_policy
        __props__["fully_qualified_domain_name"] = fully_qualified_domain_name
        __props__["identity"] = identity
        __props__["location"] = location
        __props__["name"] = name
        __props__["public_network_access_enabled"] = public_network_access_enabled
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        __props__["version"] = version
        return Server(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

