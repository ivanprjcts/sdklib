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

    def test_get_http_response(self):
        response = self.github_com_har.log.entries[0].response
        self.assertEqual(16521, response.body_size)
        self.assertEqual(200, response.status)
