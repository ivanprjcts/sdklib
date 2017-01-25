# -*- coding: utf-8 -*-

"""
Do HTTP API requests easily using Gherkin language.
"""

import json

from behave import given, when

from sdklib.http import HttpRequestContext, HttpSdk
from sdklib.http.authorization import BasicAuthentication, X11PathsAuthentication
from sdklib.http.renderers import FormRenderer, JSONRenderer

__all__ = ('set_default_host', 'set_default_proxy', 'set_url_path', 'set_url_path_with_params',
           'set_authorization_basic', 'set_11path_authorization', 'set_headers', 'set_query_parameters',
           'set_body_parameters', 'set_form_parameters', 'set_body_files', 'send_http_request',
           'send_http_request_with_query_parameters', 'send_http_request_with_form_parameters',
           'send_http_request_with_body_parameters')


def safe_add_http_request_context_to_behave_context(context):
    if not hasattr(context, "http_request_context"):
        context.http_request_context = HttpRequestContext()


@given('The API endpoint "{host}"')
def set_default_host(context, host):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.host = host


@given('The API proxy "{host}"')
def set_default_proxy(context, host):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.proxy = host


@given('The API resource "{url_path}"')
def set_url_path(context, url_path):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.url_path = url_path


@given('The parameterized API resource "{url_path_str_format}" with these parameter values')
def set_url_path_with_params(context, url_path_str_format):
    """
    Parameters:

        +------+--------+
        | key  | value  |
        +======+========+
        | key1 | value1 |
        +------+--------+
        | key2 | value2 |
        +------+--------+
    """
    safe_add_http_request_context_to_behave_context(context)
    table_as_json = dict(context.table)
    url_path = url_path_str_format % table_as_json
    context.http_request_context.url_path = url_path


@given('Authorization-Basic with username "{username}" and password "{password}"')
def set_authorization_basic(context, username, password):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.authentication_instances.append(BasicAuthentication(username=username, password=password))


@given('11Paths-Authorization with application id "{app_id}" and secret "{secret}"')
def set_11path_authorization(context, app_id, secret):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.authentication_instances.append(X11PathsAuthentication(app_id=app_id, secret=secret))


@given('The headers')
def set_headers(context):
    """
    Parameters:

        +--------------+---------------+
        | header_name  | header_value  |
        +==============+===============+
        | header1      | value1        |
        +--------------+---------------+
        | header2      | value2        |
        +--------------+---------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    headers = dict()
    for row in context.table:
        headers[row["header_name"]] = row["header_value"]
        context.http_request_context.headers = headers


@given('The query parameters')
def set_query_parameters(context):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.query_params = get_parameters(context)


@given('The body parameters')
def set_body_parameters(context):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.body_params = get_parameters(context)


@given('The form parameters')
def set_form_parameters(context):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.body_params = get_parameters(context)
    context.http_request_context.renderer = FormRenderer()


def get_parameters(context):
    """
    Reads parameters from context table

    :param context: behave context
    :return: dict with parameters names and values
    """
    return {row['param_name']: row['param_value'] for row in context.table}


@given('The body files')
def set_body_files(context):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | path_to_file |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    files = dict()
    for row in context.table:
        files[row["param_name"]] = row["path_to_file"]
        context.http_request_context.files = files


@given('The default renderer')
def set_default_renderer(context):
    """
    Set default renderer

    :param context: behave context
    """
    context.http_request_context.renderer = None


@when('I send a HTTP "{method}" request')
def send_http_request(context, method):
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.method = method
    context.api_response = HttpSdk.http_request_from_context(context.http_request_context)
    context.http_request_context.clear()


@when('I send a HTTP "{method}" request with query parameters')
def send_http_request_with_query_parameters(context, method):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    set_query_parameters(context)
    send_http_request(context, method)


@when('I send a HTTP "{method}" request with body parameters')
def send_http_request_with_body_parameters(context, method):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    set_body_parameters(context)
    send_http_request(context, method)


@when('I send a HTTP "{method}" request with form parameters')
def send_http_request_with_form_parameters(context, method):
    """
    Parameters:

        +-------------+--------------+
        | param_name  | param_value  |
        +=============+==============+
        | param1      | value1       |
        +-------------+--------------+
        | param2      | value2       |
        +-------------+--------------+
    """
    safe_add_http_request_context_to_behave_context(context)
    set_form_parameters(context)
    send_http_request(context, method)


@when('I send a HTTP "{method}" request with body parameters encoded "{encoding_type}"')
def send_http_request_with_body_parameters_encoded(context, method, encoding_type):
    pass


@when('I send a HTTP "{method}" request with this body "{resource_file}"')
def send_http_request_with_body_resource_file(context, method, resource_file):
    pass


@when('I send a HTTP "{method}" request with this JSON')
def send_http_request_with_json(context, method):
    """
    Parameters:

        .. code-block:: json

            {
                "param1": "value1",
                "param2": "value2",
                "param3": {
                    "param31": "value31"
                }
            }
    """
    safe_add_http_request_context_to_behave_context(context)
    context.http_request_context.body_params = json.loads(context.text)
    context.http_request_context.renderer = JSONRenderer()
    send_http_request(context, method)


@when('I send a HTTP "{method}" request with this XML')
def send_http_request_with_xml(context, method):
    pass
