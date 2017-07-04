from behave import given, when, then
from sdklib.behave.steps import *


@given('The cleanId as query param')
def step_impl(context):
    context.http_request_context.query_params = {"cleanId": context.clean_id}


@given('The analyzeId as query param')
def step_impl(context):
    context.http_request_context.query_params = {"analyzeId": context.analyze_id}


@then('The response contains a cleanId')
def step_impl(context):
    assert "Data" in context.api_response.json
    assert "cleanId" in context.api_response.json["Data"]
    context.clean_id = context.api_response.json["Data"]["cleanId"]


@then('The response contains an analyzeId')
def step_impl(context):
    assert "Data" in context.api_response.json
    assert "analyzeId" in context.api_response.json["Data"]
    context.analyze_id = context.api_response.json["Data"]["analyzeId"]


@then('The response contains some data')
def step_impl(context):
    assert "Data" in context.api_response.json
