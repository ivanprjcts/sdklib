import json

from behave import given, when, then

from sdklib.http import api, HttpRequestContextSingleton
from sdklib.http.authorization import BasicAuthentication, X11PathsAuthentication


@given('The API endpoint "{host}"')
def set_default_host(context, host):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.host = host


@given('The API proxy "{host}"')
def set_default_proxy(context, host):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.proxy = host


@given('The API resource "{url_path}"')
def set_url_path(context, url_path):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.url_path = url_path


@given('The parameterized API resource "{url_path_str_format}" with these parameter values')
def set_url_path_with_params(context, url_path_str_format):
    table_as_json = dict(context.table)
    url_path = url_path_str_format % table_as_json
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.url_path = url_path


@given('Authorization-Basic with username "{username}" and password "{password}"')
def set_authorization_basic(context, username, password):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.authentication_instances.append(BasicAuthentication(username=username, password=password))


@given('11Paths-Authorization with application id "{app_id}" and secret "{secret}"')
def set_11path_authorization(context, app_id, secret):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.authentication_instances.append(X11PathsAuthentication(app_id=app_id, secret=secret))


@given('The headers')
def set_headers(context):
    headers = dict()
    for row in context.table:
        headers[row["header_name"]] = row["header_value"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.headers = headers


@given('The query parameters')
def set_query_parameters(context):
    query_params = dict()
    for row in context.table:
        query_params[row["param_name"]] = row["param_value"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.query_params = query_params


@given('The body parameters')
def set_body_parameters(context):
    body_params = dict()
    for row in context.table:
        body_params[row["param_name"]] = row["param_value"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.body_params = body_params


@given('The body files')
def set_body_files(context):
    files = dict()
    for row in context.table:
        files[row["param_name"]] = row["path_to_file"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.files = files


@when('I send a HTTP "{method}" request')
def send_http_request(context, method):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.method = method
    context.api_response = api.http_request_from_context(http_request_context)
    http_request_context.clear()


@when('I send a HTTP "{method}" request with query parameters')
def send_http_request_with_query_parameters(context, method):
    query_params = dict()
    for row in context.table:
        query_params[row["param_name"]] = row["param_value"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.method = method
    http_request_context.query_params = query_params
    context.api_response = api.http_request_from_context(http_request_context)
    http_request_context.clear()


@when('I send a HTTP "{method}" request with body parameters')
def send_http_request_with_body_parameters(context, method):
    body_params = dict()
    for row in context.table:
        body_params[row["param_name"]] = row["param_value"]
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.method = method
    http_request_context.body_params = body_params
    context.api_response = api.http_request_from_context(http_request_context)
    http_request_context.clear()


@when('I send a HTTP "{method}" request with body parameters encoded "{encoding_type}"')
def send_http_request_with_body_parameters_encoded(context, method, encoding_type):
    pass


@when('I send a HTTP "{method}" request with this body "{resource_file}"')
def send_http_request_with_body_resource_file(context, method, resource_file):
    pass


@when('I send a HTTP "{method}" request with this JSON')
def send_http_request_with_json(context, method):
    pass


@when('I send a HTTP "{method}" request with this XML')
def send_http_request_with_xml(context, method):
    pass


@then('The HTTP status code should be "{code}"')
def http_status_code_should_be(context, code):
    assert(context.api_response.status == int(code))


@then('The HTTP status code should not be "{code}"')
def http_status_code_not_should_be(context, code):
    assert(context.api_response.status != int(code))


@then('The HTTP reason phrase should be "{reason}"')
def http_reason_phrase_should_be(context, reason):
    assert(context.api_response.reason == reason)


@then('The HTTP reason phrase should contain "{reason}"')
def http_reason_phrase_should_not_be(context, reason):
    assert (context.api_response.reason != reason)


@then('The response header "{header_name}" should be "{header_value}"')
def http_response_header_should_be(context, header_name, header_value):
    pass


@then('The response header "{header_name}" should contain "{header_value}"')
def http_response_header_should_contain(context, header_name, header_value):
    pass


@then('The response body should contain this parameters')
def http_response_body_should_contain_this_parameters(context):
    pass


@then('The response body should be this "{response_file}"')
def http_response_body_should_be_this_file(context, response_file):
    pass


@then('The response body should be this JSON')
def http_response_body_should_be_this_json(context):
    body_params = json.loads(context.text)
    assert(body_params == context.api_response.data)


@then('The response body should be this XML')
def http_response_body_should_be_this_xml(context):
    pass
