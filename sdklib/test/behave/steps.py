from behave import given, when, then

from sdklib.http import api, HttpRequestContextSingleton


@given('The API endpoint "{host}"')
def set_default_host(context, host):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.host = host


@given('The final API resource "{url_path}"')
def set_url_path(context, url_path):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.url_path = url_path


@given('The API resource "{url_path_str_format}" with these parameter values')
def set_url_path_with_params(context, url_path_str_format):
    table_as_json = dict(context.table)
    url_path = url_path_str_format % table_as_json
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.url_path = url_path


@given('Authorization-Basic with username "{username}" and password "{password}"')
def set_authorization_basic(context, username, password):
   pass


@given('11Paths-Authorization with application id "{app_id}" and secret "{secret}"')
def set_11path_authorization(context, app_id, secret):
   pass


@given('The headers:')
def set_headers(context, headers):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.headers = headers


@given('The query parameters:')
def set_query_parameters(context, parameters):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.query_parameters = parameters


@given('The body parameters:')
def set_body_parameters(context, parameters):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.body_parameters = parameters


@given('The body files:')
def set_body_files(context, files):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.files = files


@when('I send a HTTP "{method}" request')
def send_http_request(context, method):
    http_request_context = HttpRequestContextSingleton.get_instance()
    http_request_context.method = method
    context.api_response = api.http_request_from_context(http_request_context)


@when('I send a HTTP "{method}" request with query parameters')
def send_http_request_with_query_parameters(context, method):
   assert(method in ["allowed methods variable"])


@when('I send a HTTP "{method}" request with body parameters')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@when('I send a HTTP "{method}" request with body parameters encoded "{encoding_type}"')
def send_http_request_with_body_parameters(context, method, encoding_type):
   assert(method in ["allowed methods variable"])


@when('I send a HTTP "{method}" request with this body "{resource_file}"')
def send_http_request_with_body_parameters(context, method, resource_file):
   assert(method in ["allowed methods variable"])


@when('I send a HTTP "{method}" request with this JSON:')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@when('I send a HTTP "{method}" request with this XML:')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The HTTP status code should be "{code}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The HTTP status code should not be "{code}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The HTTP reason phrase should be "{phrase}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The HTTP reason phrase should contain "{phrase}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response header "{header_name}" should be "{header_value}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response header "{header_name}" should contain "{header_value}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response body should contain this parameters:')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response body should be this "{response_file}"')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response body should be this JSON:')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])


@then('The response body should be this XML:')
def send_http_request_with_body_parameters(context, method):
   assert(method in ["allowed methods variable"])
