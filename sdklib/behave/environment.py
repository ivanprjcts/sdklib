# -*- coding: utf-8 -*-

from sdklib.behave.requests import safe_add_http_request_context_to_behave_context


def sdklib_before_all(context):
    """
    Initialization method that will be executed before all execution.

    :param context:
    :return:
    """
    safe_add_http_request_context_to_behave_context(context)


def sdklib_after_scenario(context, scenario):
    """
    Clean method that will be executed after each scenario.

    :param context:
    :param scenario:
    :return:
    """
    context.http_request_context.clear()
