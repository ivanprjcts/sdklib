# -*- coding: utf-8 -*-

import unittest

from sdklib.http import HttpRequestContext
from sdklib.http.authorization import basic_authentication, x_11paths_authentication


class TestAuthorization(unittest.TestCase):

    def test_basic_authentication(self):
        value = basic_authentication(username=b"Aladdin", password=b"OpenSesame")
        self.assertEqual(b"Basic QWxhZGRpbjpPcGVuU2VzYW1l", value)

    def test_11paths_authentication(self):
        context = HttpRequestContext(method="GET", url_path="/path/")
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", context=context,
                                                           utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 t0cS2yvvlcSqiKVK/v6tjG8pP4s=", header_value)
        self.assertEqual("2016-01-01 00:00:00", date_time)

    def test_11paths_authentication_now(self):
        context = HttpRequestContext(method="GET", url_path="/path/")
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", context=context)
        self.assertIn("11PATHS 123456 ", header_value)
        self.assertNotEqual("11PATHS 123456 t0cS2yvvlcSqiKVK/v6tjG8pP4s=", header_value)
        self.assertNotEqual("2016-01-01 00:00:00", date_time)

    def test_11paths_authentication_with_query_params(self):
        context = HttpRequestContext(method="GET", url_path="/path/",
                                     query_params={"param": "value"})
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", context=context,
                                                           utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 kVXKo1ug8GRm0kyAjvruvtNDetU=", header_value)
        self.assertEqual("2016-01-01 00:00:00", date_time)

    def test_11paths_authentication_with_body(self):
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     body_params={"param": "value"})
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", context=context,
                                                           utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 8Ok3S1xUFLtjRxRkWVoZAKXZc1A=", header_value)
        self.assertEqual("2016-01-01 00:00:00", date_time)
