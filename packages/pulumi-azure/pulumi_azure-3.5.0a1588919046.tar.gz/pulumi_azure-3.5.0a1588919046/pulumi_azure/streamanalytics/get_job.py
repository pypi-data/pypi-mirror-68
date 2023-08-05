# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetJobResult:
    """
    A collection of values returned by getJob.
    """
    def __init__(__self__, compatibility_level=None, data_locale=None, events_late_arrival_max_delay_in_seconds=None, events_out_of_order_max_delay_in_seconds=None, events_out_of_order_policy=None, id=None, job_id=None, location=None, name=None, output_error_policy=None, resource_group_name=None, streaming_units=None, transformation_query=None):
        if compatibility_level and not isinstance(compatibility_level, str):
            raise TypeError("Expected argument 'compatibility_level' to be a str")
        __self__.compatibility_level = compatibility_level
        """
        The compatibility level for this job.
        """
        if data_locale and not isinstance(data_locale, str):
            raise TypeError("Expected argument 'data_locale' to be a str")
        __self__.data_locale = data_locale
        """
        The Data Locale of the Job.
        """
        if events_late_arrival_max_delay_in_seconds and not isinstance(events_late_arrival_max_delay_in_seconds, float):
            raise TypeError("Expected argument 'events_late_arrival_max_delay_in_seconds' to be a float")
        __self__.events_late_arrival_max_delay_in_seconds = events_late_arrival_max_delay_in_seconds
        """
        The maximum tolerable delay in seconds where events arriving late could be included.
        """
        if events_out_of_order_max_delay_in_seconds and not isinstance(events_out_of_order_max_delay_in_seconds, float):
            raise TypeError("Expected argument 'events_out_of_order_max_delay_in_seconds' to be a float")
        __self__.events_out_of_order_max_delay_in_seconds = events_out_of_order_max_delay_in_seconds
        """
        The maximum tolerable delay in seconds where out-of-order events can be adjusted to be back in order.
        """
        if events_out_of_order_policy and not isinstance(events_out_of_order_policy, str):
            raise TypeError("Expected argument 'events_out_of_order_policy' to be a str")
        __self__.events_out_of_order_policy = events_out_of_order_policy
        """
        The policy which should be applied to events which arrive out of order in the input event stream.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        The provider-assigned unique ID for this managed resource.
        """
        if job_id and not isinstance(job_id, str):
            raise TypeError("Expected argument 'job_id' to be a str")
        __self__.job_id = job_id
        """
        The Job ID assigned by the Stream Analytics Job.
        """
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        __self__.location = location
        """
        The Azure location where the Stream Analytics Job exists.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if output_error_policy and not isinstance(output_error_policy, str):
            raise TypeError("Expected argument 'output_error_policy' to be a str")
        __self__.output_error_policy = output_error_policy
        """
        The policy which should be applied to events which arrive at the output and cannot be written to the external storage due to being malformed (such as missing column values, column values of wrong type or size). 
        """
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        __self__.resource_group_name = resource_group_name
        if streaming_units and not isinstance(streaming_units, float):
            raise TypeError("Expected argument 'streaming_units' to be a float")
        __self__.streaming_units = streaming_units
        """
        The number of streaming units that the streaming job uses.
        """
        if transformation_query and not isinstance(transformation_query, str):
            raise TypeError("Expected argument 'transformation_query' to be a str")
        __self__.transformation_query = transformation_query
        """
        The query that will be run in the streaming job, [written in Stream Analytics Query Language (SAQL)](https://msdn.microsoft.com/library/azure/dn834998).
        """
class AwaitableGetJobResult(GetJobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobResult(
            compatibility_level=self.compatibility_level,
            data_locale=self.data_locale,
            events_late_arrival_max_delay_in_seconds=self.events_late_arrival_max_delay_in_seconds,
            events_out_of_order_max_delay_in_seconds=self.events_out_of_order_max_delay_in_seconds,
            events_out_of_order_policy=self.events_out_of_order_policy,
            id=self.id,
            job_id=self.job_id,
            location=self.location,
            name=self.name,
            output_error_policy=self.output_error_policy,
            resource_group_name=self.resource_group_name,
            streaming_units=self.streaming_units,
            transformation_query=self.transformation_query)

def get_job(name=None,resource_group_name=None,opts=None):
    """
    Use this data source to access information about an existing Stream Analytics Job.




    :param str name: Specifies the name of the Stream Analytics Job.
    :param str resource_group_name: Specifies the name of the resource group the Stream Analytics Job is located in.
    """
    __args__ = dict()


    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:streamanalytics/getJob:getJob', __args__, opts=opts).value

    return AwaitableGetJobResult(
        compatibility_level=__ret__.get('compatibilityLevel'),
        data_locale=__ret__.get('dataLocale'),
        events_late_arrival_max_delay_in_seconds=__ret__.get('eventsLateArrivalMaxDelayInSeconds'),
        events_out_of_order_max_delay_in_seconds=__ret__.get('eventsOutOfOrderMaxDelayInSeconds'),
        events_out_of_order_policy=__ret__.get('eventsOutOfOrderPolicy'),
        id=__ret__.get('id'),
        job_id=__ret__.get('jobId'),
        location=__ret__.get('location'),
        name=__ret__.get('name'),
        output_error_policy=__ret__.get('outputErrorPolicy'),
        resource_group_name=__ret__.get('resourceGroupName'),
        streaming_units=__ret__.get('streamingUnits'),
        transformation_query=__ret__.get('transformationQuery'))
