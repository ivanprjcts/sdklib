# -*- coding: utf-8 -*-

import unittest

from sdklib.http import HttpRequestContext
from sdklib.http.authorization import (
    basic_authorization, x_11paths_authorization, X11PathsAuthentication, BasicAuthentication,
    _get_11paths_serialized_headers
)
from sdklib.http.renderers import FormRenderer, JSONRenderer, MultiPartRenderer
from sdklib.http.headers import AUTHORIZATION_HEADER_NAME, X_11PATHS_BODY_HASH_HEADER_NAME


class TestAuthorization(unittest.TestCase):

    def test_basic_authentication(self):
        value = basic_authorization(username="Aladdin", password="OpenSesame")
        self.assertEqual("Basic QWxhZGRpbjpPcGVuU2VzYW1l", value)

    def test_basic_authentication_class(self):
        a = BasicAuthentication("Aladdin", "OpenSesame")
        ctx = HttpRequestContext(headers={})
        auth_ctx = a.apply_authentication(context=ctx)
        self.assertEqual("Basic QWxhZGRpbjpPcGVuU2VzYW1l", auth_ctx.headers[AUTHORIZATION_HEADER_NAME])

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

    def test_11paths_authentication_with_multiples_query_params(self):
        context = HttpRequestContext(method="GET", url_path="/path/",
                                     query_params={"param1": "value1", "param2": "value2"})
        header_value1 = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                                utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 pof/ZVaAmmrbSOCJXiRWuQ5vrco=", header_value1)

        context = HttpRequestContext(method="GET", url_path="/path/",
                                     query_params={"param2": "value2", "param1": "value1"})
        header_value2 = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                                utc="2016-01-01 00:00:00")
        self.assertEqual(header_value1, header_value2)

    def test_11paths_authentication_with_body(self):
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     body_params={"param": "value"}, renderer=FormRenderer())
        header_value = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                               utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 8Ok3S1xUFLtjRxRkWVoZAKXZc1A=", header_value)

    def test_11paths_authentication_with_json_body(self):
        context = HttpRequestContext(method="POST", url_path="/path/",
                                     headers={"Content-Type": "application/json"},
                                     body_params={"param": "value"}, renderer=JSONRenderer())
        header_value = x_11paths_authorization(app_id="123456", secret="654321", context=context,
                                               utc="2016-01-01 00:00:00")
        self.assertEqual("11PATHS 123456 VXVXfFsBVfCIwheS/27C8DqqpfQ=", header_value)

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
        self.assertEqual("11PATHS QRKJw6qX4fykZ3G3yqkQ CMf3royzdD4l/P0RVKyr2uOXZ4Y=", res_context.headers[AUTHORIZATION_HEADER_NAME])

    def test_11paths_authentication_class_json(self):
        auth = X11PathsAuthentication(app_id="123456", secret="654321", utc="2016-01-01 00:00:00")
        context = HttpRequestContext(method="POST", url_path="/path/", headers={"Content-Type": "application/json"},
                                     body_params={"param": "value"}, renderer=JSONRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 123456 6CFsVmrRxEz3Icz6U8SSHZ4RukE=", res_context.headers[AUTHORIZATION_HEADER_NAME])
        self.assertEqual("f247c7579b452d08f38eec23c2d1a4a23daee0d2", res_context.headers[X_11PATHS_BODY_HASH_HEADER_NAME])

    def test_11paths_authentication_class_json_ignorecase_header_name(self):
        auth = X11PathsAuthentication(app_id="123456", secret="654321", utc="2016-01-01 00:00:00")
        context = HttpRequestContext(method="POST", url_path="/path/", headers={"Content-type": "application/json"},
                                     body_params={"param": "value"}, renderer=JSONRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 123456 6CFsVmrRxEz3Icz6U8SSHZ4RukE=", res_context.headers[AUTHORIZATION_HEADER_NAME])
        self.assertEqual("f247c7579b452d08f38eec23c2d1a4a23daee0d2", res_context.headers[X_11PATHS_BODY_HASH_HEADER_NAME])

    def test_11paths_authentication_get_serialized_headers(self):
        serializer_headers = _get_11paths_serialized_headers(
            {
                "X-11Paths-profile-id": "77ed609a-1a9b-4c16-97c2-ba32f72f5499",
                "X-11paths-file-hash": "a30d2aef3f9da7f3273100bb7d412ccedb4c481f"
            }
        )
        self.assertEqual(
            "x-11paths-file-hash:a30d2aef3f9da7f3273100bb7d412ccedb4c481f x-11paths-profile-id:77ed609a-1a9b-4c16-97c2-ba32f72f5499",
            serializer_headers
        )

    def test_11paths_authentication_class_multiples_headers(self):
        auth = X11PathsAuthentication(app_id="2kNhWLEETQ46KWLnAg48", secret="lBc4BSeqCGkidJZXictc3yiHbKBS87hjE05YrswJ",
                                      utc="2017-01-27 08:27:44")
        context = HttpRequestContext(method="POST", url_path="/ExternalApi/CleanFile",
                                     renderer=MultiPartRenderer(),
                                     headers={"X-11paths-profile-id": "77ed609a-1a9b-4c16-97c2-ba32f72f5499",
                                              "Content-Type": "multipart/form-data"},
                                     files={"file": "tests/resources/file.png"})
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 2kNhWLEETQ46KWLnAg48 8/fuEv9NLn41ikh96hRHMFGs1ww=", res_context.headers["Authorization"])

    def test_11paths_authentication_post_empty_body_params(self):
        auth = X11PathsAuthentication(app_id="2kNhWLEETQ46KWLnAg48", secret="lBc4BSeqCGkidJZXictc3yiHbKBS87hjE05YrswJ",
                                      utc="2017-01-27 08:27:44")
        context = HttpRequestContext(method="POST", url_path="/ExternalApi/CleanFile",
                                     renderer=JSONRenderer())
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 2kNhWLEETQ46KWLnAg48 atYkLRYJ3b+CXU+GdklyALAr9NE=",
                         res_context.headers["Authorization"])
        self.assertNotIn(X_11PATHS_BODY_HASH_HEADER_NAME, res_context.headers)
        self.assertEqual("application/x-www-form-urlencoded", res_context.headers["Content-Type"])

    def test_11paths_authentication_post_json_empty_body_params(self):
        auth = X11PathsAuthentication(app_id="2kNhWLEETQ46KWLnAg48", secret="lBc4BSeqCGkidJZXictc3yiHbKBS87hjE05YrswJ",
                                      utc="2017-01-27 08:27:44")
        context = HttpRequestContext(method="POST", url_path="/ExternalApi/CleanFile",
                                     headers={"Content-Type": "application/json"})
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 2kNhWLEETQ46KWLnAg48 u/91oWtEs2qkco5v6JXcfWx+FJ0=",
                         res_context.headers["Authorization"])
        self.assertEqual("application/json", res_context.headers["Content-Type"])
        self.assertEqual("da39a3ee5e6b4b0d3255bfef95601890afd80709", res_context.headers["X-11paths-body-hash"])

    def test_11paths_authentication_post_json_body_params(self):
        auth = X11PathsAuthentication(app_id="2kNhWLEETQ46KWLnAg48", secret="lBc4BSeqCGkidJZXictc3yiHbKBS87hjE05YrswJ",
                                      utc="2017-01-27 08:27:44")
        context = HttpRequestContext(method="POST", url_path="/ExternalApi/CleanFile",
                                     body_params={"param": "value"},
                                     headers={"Content-Type": "application/json"})
        res_context = auth.apply_authentication(context=context)
        self.assertEqual("11PATHS 2kNhWLEETQ46KWLnAg48 zvsWw6S2XZpke6rSvdpe0swlOIc=",
                         res_context.headers["Authorization"])
        self.assertEqual("application/json", res_context.headers["Content-Type"])
        self.assertEqual("f247c7579b452d08f38eec23c2d1a4a23daee0d2", res_context.headers["X-11paths-body-hash"])
