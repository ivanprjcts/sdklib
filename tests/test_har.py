import unittest

from sdklib.http import HttpSdk
from sdklib.http.har import HAR, sequential_requests
from sdklib.http.renderers import default_renderer


class TestHAR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/resources/github.com.har", "r") as f:
            cls.github_com_har = HAR(f.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_har_file(self):
        self.assertEqual(23, len(self.github_com_har.log.entries))
        self.assertEqual("GET", self.github_com_har.log.entries[0].request.method)
        self.assertEqual("https://github.com/ivanprjcts/sdklib", self.github_com_har.log.entries[0].request.url)

    def test_get_http_request_context(self):
        self.assertEqual(23, len(self.github_com_har.log.entries))
        self.assertEqual("GET", self.github_com_har.log.entries[0].request.method)
        self.assertEqual("https://github.com/ivanprjcts/sdklib", self.github_com_har.log.entries[0].request.url)

        http_request_context = self.github_com_har.log.entries[0].request.as_http_request_context()
        self.assertEqual("GET", http_request_context.method)
        self.assertEqual("https://github.com", http_request_context.host)
        self.assertTrue(isinstance(http_request_context.renderer, type(default_renderer)))

        HttpSdk.http_request_from_context(http_request_context)

    def test_sequential_requests(self):
        request_responses = sequential_requests(self.github_com_har.log.entries[:2])
        self.assertEqual("GET", request_responses[0][0].method)
        self.assertEqual("https://github.com", request_responses[0][0].host)
        self.assertTrue(isinstance(request_responses[0][0].renderer, type(default_renderer)))

    def test_get_http_response(self):
        response = self.github_com_har.log.entries[0].response
        self.assertEqual(16521, response.body_size)
        self.assertEqual(200, response.status)
