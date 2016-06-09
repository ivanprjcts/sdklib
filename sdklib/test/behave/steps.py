from behave import given, when, then

from sdklib.http.sdk_base import HttpSdk


@given('The API endpoint "{host}"')
def set_default_host(context, host):
    HttpSdk.set_default_host(host)


@given('The API resource "{url_path}"')
def set_url_path(context, url_path):
    pass


@given('The API resource "{url_path_regex}" with these parameter values:')
def set_url_path(context, url_path_regex, values):
    pass


@given('Authorization-Basic with username "{username}" and password "{password}"')
def set_authorization_basic(context, username, password):
   pass


@given('11Paths-Authorization with application id "{app_id}" and secret "{secret}"')
def set_11path_authorization(context, app_id, secret):
   pass


@given('The headers:')
def set_headers(context, headers):
   pass


@given('The query parameters:')
def set_query_parameters(context, parameters):
   pass


@given('The body parameters:')
def set_body_parameters(context, parameters):
   pass


@given('The body files:')
def set_body_files(context, files):
   pass


@when('I send a HTTP "{method}" request # methods: GET, POST, PUT, PATCH, DELETE')
def send_http_request(context, method):
   assert(method in ["allowed methods variable"])


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
