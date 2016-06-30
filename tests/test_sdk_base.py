import unittest

from sdklib.http import HttpSdk


class TestSdkBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_set_default_host_without_scheme(self):
        HttpSdk.set_default_host("localhost:1234")
        api = HttpSdk()
        self.assertEqual(api.DEFAULT_HOST, "http://localhost:1234")

    def test_set_default_proxy_without_scheme(self):
        HttpSdk.set_default_proxy("localhost:1234")
        api = HttpSdk()
        self.assertEqual(api.DEFAULT_PROXY, "http://localhost:1234")
