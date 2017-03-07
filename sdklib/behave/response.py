# -*- coding: utf-8 -*-

"""
Verify HTTP responses easily using Gherkin language.
"""

import json

from behave import then

__all__ = ('http_status_code_should_be', 'http_status_code_not_should_be', 'http_reason_phrase_should_be',
           'http_reason_phrase_should_not_be', 'http_reason_phrase_should_contain',
           'http_response_body_should_be_this_json')


@then('The HTTP status code should be "{code:d}"')
def http_status_code_should_be(context, code):
    assert context.api_response.status == code, \
        "Expected: {}; Message: {}".format(code, context.api_response.status)


@then('The HTTP status code should not be "{code:d}"')
def http_status_code_not_should_be(context, code):
    assert(context.api_response.status != code)


@then('The HTTP reason phrase should be "{reason}"')
def http_reason_phrase_should_be(context, reason):
    assert(context.api_response.reason == reason)


@then('The HTTP reason phrase should not be "{reason}"')
def http_reason_phrase_should_not_be(context, reason):
    assert context.api_response.reason != reason, "%s is equal to %s" % (context.api_response.reason, reason)


@then('The HTTP reason phrase should contain "{reason}"')
def http_reason_phrase_should_contain(context, reason):
    assert reason in context.api_response.reason, "%s should contain %s" % (context.api_response.reason, reason)


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
    body_params = json.loads(context.text)
    assert body_params == context.api_response.data, \
        "Expected: {}; Message: {}".format(body_params, context.api_response.data)


@then('The response body should be this XML')
def http_response_body_should_be_this_xml(context):
    pass
