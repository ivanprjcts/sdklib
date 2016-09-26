# -*- coding: utf-8 -*-

import unittest

from sdklib.http import HttpRequestContext
from sdklib.http.authorization import basic_authorization, x_11paths_authorization
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