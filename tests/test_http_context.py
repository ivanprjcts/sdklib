import unittest

from sdklib.http import HttpRequestContextSingleton, HttpRequestContext


class TestHttpContext(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_http_context_sigleton(self):
        ctxt_singleton = HttpRequestContextSingleton.get_instance()
        ctxt_singleton.method = "POST"

        ctxt_singleton2 = HttpRequestContextSingleton.get_instance()
        self.assertEqual(ctxt_singleton.method, ctxt_singleton2.method)

    def test_http_context_singleton_clear(self):
        ctxt_singleton = HttpRequestContextSingleton.get_instance()
        ctxt_singleton.method = "POST"
        self.assertEqual("POST", ctxt_singleton.method)
        ctxt_singleton.clear()
        self.assertNotEqual("POST", ctxt_singleton.method)

        ctxt_singleton2 = HttpRequestContextSingleton.get_instance()
        self.assertNotEqual("POST", ctxt_singleton2.method)

    def test_http_context_singleton_fields_to_clear(self):
        ctxt_singleton = HttpRequestContextSingleton.get_instance()
        ctxt_singleton.fields_to_clear = ['proxy']

        ctxt_singleton.proxy = "http://localhost:8080"
        ctxt_singleton.method = "PUT"
        self.assertEqual("http://localhost:8080", ctxt_singleton.proxy)
        ctxt_singleton.clear()
        self.assertNotEqual("http://localhost:8080", ctxt_singleton.proxy)
        self.assertEqual("PUT", ctxt_singleton.method)

        ctxt_singleton2 = HttpRequestContextSingleton.get_instance()
        self.assertNotEqual("http://localhost:8080", ctxt_singleton2.proxy)
        self.assertEqual("PUT", ctxt_singleton2.method)

    def test_http_context(self):
        ctxt_singleton = HttpRequestContext()
        ctxt_singleton.method = "POST"
        self.assertEqual("POST", ctxt_singleton.method)

    def test_http_context_clear(self):
        ctxt_singleton = HttpRequestContext()
        ctxt_singleton.method = "POST"
        self.assertEqual("POST", ctxt_singleton.method)
        ctxt_singleton.clear()
        self.assertNotEqual("POST", ctxt_singleton.method)

        ctxt_singleton2 = HttpRequestContext()
        self.assertNotEqual("POST", ctxt_singleton2.method)

    def test_http_context_fields_to_clear(self):
        ctxt_singleton = HttpRequestContext()
        ctxt_singleton.fields_to_clear = ['proxy']

        ctxt_singleton.proxy = "http://localhost:8080"
        ctxt_singleton.method = "PUT"
        self.assertEqual("http://localhost:8080", ctxt_singleton.proxy)
        ctxt_singleton.clear()
        self.assertNotEqual("http://localhost:8080", ctxt_singleton.proxy)
        self.assertEqual("PUT", ctxt_singleton.method)

    def test_http_context_clear_by_arg(self):
        ctxt_singleton = HttpRequestContext()
        ctxt_singleton.fields_to_clear = []

        ctxt_singleton.proxy = "http://localhost:8080"
        ctxt_singleton.method = "PUT"
        self.assertEqual("http://localhost:8080", ctxt_singleton.proxy)
        ctxt_singleton.clear("proxy")
        self.assertNotEqual("http://localhost:8080", ctxt_singleton.proxy)
        self.assertEqual("PUT", ctxt_singleton.method)

    def test_http_context_headers_none(self):
        ctxt = HttpRequestContext()
        ctxt.headers = None
        self.assertEqual({}, ctxt.headers)
