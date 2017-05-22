import unittest

from sdklib.http import HttpSdk
from sdklib.http.har import HAR
from sdklib.http.renderers import default_renderer


class TestHAR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_har_file(self):
        with open("tests/resources/github.com.har", "r") as f:
            har = HAR(f.read())
        self.assertEqual(23, len(har.log.entries))
        self.assertEqual("GET", har.log.entries[0].request.method)
        self.assertEqual("https://github.com/ivanprjcts/sdklib", har.log.entries[0].request.url)

    def test_get_http_request_context(self):
        with open("tests/resources/github.com.har", "r") as f:
            har = HAR(f.read())
        self.assertEqual(23, len(har.log.entries))
        self.assertEqual("GET", har.log.entries[0].request.method)
        self.assertEqual("https://github.com/ivanprjcts/sdklib", har.log.entries[0].request.url)

        http_request_context = har.log.entries[0].request.as_http_request_context()
        self.assertEqual("GET", http_request_context.method)
        self.assertEqual("https://github.com", http_request_context.host)
        self.assertTrue(isinstance(http_request_context.renderer, type(default_renderer)))

        HttpSdk.http_request_from_context(http_request_context)
