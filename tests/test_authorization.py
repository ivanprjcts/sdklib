# -*- coding: utf-8 -*-

import unittest

from sdklib.http import HttpRequestContext
from sdklib.http.authorization import basic_authorization, x_11paths_authorization, X11PathsAuthentication
from sdklib.http.renderers import FormRenderer


class TestAuthorization(unittest.TestCase):

    def test_basic_authentication(self):
        value = basic_authorization(username=b"Aladdin", password=b"OpenSesame")
        self.assertEqual(b"Basic QWxhZGRpbjpPcGVuU2VzYW1l", value)

    def test_11paths_authentication(self):
        context = HttpRequestContext(method="GET", url_path="/path/")
        header_value = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                                          utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 t0cS2yvvlcSqiKVK/v6tjG8pP4s=", header_value)

    def test_11paths_authentication_with_query_params(self):
        context = HttpRequestContext(method="GET", url_path="/path/",
                                     query_params={"param": "value"})
        header_value = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                                          utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 kVXKo1ug8GRm0kyAjvruvtNDetU=", header_value)

    def test_11paths_authentication_with_body(self):
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     body_params={"param": "value"}, renderer=FormRenderer())
        header_value = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                               utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 8Ok3S1xUFLtjRxRkWVoZAKXZc1A=", header_value)

    def test_11paths_authentication_class_with_static_time(self):
        auth = X11PathsAuthentication(app_id="123456", secret="654321", utc="2016-01-01 00:00:00")
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     body_params={"param": "value"}, renderer=FormRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 123456 8Ok3S1xUFLtjRxRkWVoZAKXZc1A=", res_context.headers["Authorization"])

    def test_11paths_authentication_class_with_dynamic_time(self):
        auth = X11PathsAuthentication(app_id="123456", secret="654321")
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     body_params={"param": "value"}, renderer=FormRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertNotEqual("11PATHS 123456 8Ok3S1xUFLtjRxRkWVoZAKXZc1A=", res_context.headers["Authorization"])

    def test_11paths_authentication_form_multi(self):
        auth = X11PathsAuthentication(app_id="QRKJw6qX4fykZ3G3yqkQ", secret="eHkAXTebECWBs4TtNbNMBYC99AzMrmaydUWcUFEM",
                                      utc="2016-12-12 11:18:45")
        context = HttpRequestContext(method="POST", url_path="/api/0.1/vulnerabilities/15fc104c-dc55-41d4-8d4e-4d76eda7a029/consequences",
                                     body_params={"consequence.scopes[]": "1",
                                                  "consequence.impact[]": "1",
                                                  "consequence.description[es]": "test",
                                                  "consequence.description[en]": "test"},
                                     renderer=FormRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS QRKJw6qX4fykZ3G3yqkQ CMf3royzdD4l/P0RVKyr2uOXZ4Y=", res_context.headers["Authorization"])
