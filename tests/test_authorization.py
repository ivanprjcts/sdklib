# -*- coding: utf-8 -*-

import unittest

from sdklib.http.authorization import basic_authentication, x_11paths_authentication


class TestAuthorization(unittest.TestCase):

    def test_basic_authentication(self):
        value = basic_authentication(username="Aladdin", password="OpenSesame")
        self.assertEqual("Basic QWxhZGRpbjpPcGVuU2VzYW1l", value)

    def test_11paths_authentication(self):
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", http_method="GET",
                                                           url_path_query="/path/", utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 t0cS2yvvlcSqiKVK/v6tjG8pP4s=", header_value)
        self.assertEqual("2016-01-01 00:00:00", date_time)

    def test_11paths_authentication_now(self):
        header_value, date_time = x_11paths_authentication(app_id="123456", secret="654321", http_method="GET",
                                                           url_path_query="/path/")
        self.assertIn("11PATHS 123456 ", header_value)
        self.assertNotEqual("11PATHS 123456 t0cS2yvvlcSqiKVK/v6tjG8pP4s=", header_value)
        self.assertNotEqual("2016-01-01 00:00:00", date_time)