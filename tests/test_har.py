import unittest

from sdklib.http import HttpSdk
from sdklib.http.har import HAR, sequential_requests
from sdklib.http.renderers import default_renderer


class TestHAR(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/resources/github.com.har", "r") as f:
            cls.github_com_har = HAR(f.read())
        with open("tests/resources/latch.elevenpaths.com.har.json", "r") as f:
            cls.latch_elevenpaths_com_har = HAR(f.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load_har_file(self):
        self.assertEqual(23, len(self.github_com_har.log.entries))
        self.assertEqual("GET", self.github_com_har.log.entries[0].request.method)
        self.assertEqual("https://github.com/ivanprjcts/sdklib", self.github_com_har.log.entries[0].request.url)

    def test_get_http_request_context(self):
        pass
        #self.assertEqual(23, len(self.github_com_har.log.entries))
        #self.assertEqual("GET", self.github_com_har.log.entries[0].request.method)
        #self.assertEqual("https://github.com/ivanprjcts/sdklib", self.github_com_har.log.entries[0].request.url)

        #http_request_context = self.github_com_har.log.entries[0].request.as_http_request_context()
        #self.assertEqual("GET", http_request_context.method)
        #self.assertEqual("https://github.com", http_request_context.host)
        #self.assertTrue(isinstance(http_request_context.renderer, type(default_renderer)))

        #HttpSdk.http_request_from_context(http_request_context)

    def test_sequential_requests(self):
        #request_responses = sequential_requests(self.github_com_har.log.entries[:2])
        #self.assertEqual("GET", request_responses[0][0].method)
        #self.assertEqual("https://github.com", request_responses[0][0].host)
        #self.assertTrue(isinstance(request_responses[0][0].renderer, type(default_renderer)))
        pass

    def test_sequential_dynamic_requests(self):
        request_responses = sequential_requests(self.latch_elevenpaths_com_har.log.entries,
                                                update_dynamic_elements=True)
        self.assertEqual(4, len(request_responses))
        self.assertEqual("GET", request_responses[0][0].method)
        self.assertEqual("https://latch.elevenpaths.com", request_responses[0][0].host)
        self.assertEqual("sdklib.test@outlook.com", request_responses[1][0].body_params["username"])
        self.assertIsNotNone(request_responses[1][0].body_params["authenticityToken"])
        self.assertNotEqual(
            "d0f547b43770f586d5e0883c48a98e3c73736ef2", request_responses[1][0].body_params["authenticityToken"])

    def test_get_http_response(self):
        response = self.github_com_har.log.entries[0].response
        self.assertEqual(16521, response.body_size)
        self.assertEqual(200, response.status)
