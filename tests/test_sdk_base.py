import unittest

from sdklib.http import HttpSdk


class MyIncognitoClass(HttpSdk):
    incognito_mode = True


class TestSdkBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.my_incognito_class = MyIncognitoClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_set_default_host_without_scheme(self):
        default_host = HttpSdk.DEFAULT_HOST
        HttpSdk.set_default_host("localhost:1234")
        self.assertEqual(HttpSdk.DEFAULT_HOST, "http://localhost:1234")
        HttpSdk.set_default_host(default_host)
        self.assertEqual(HttpSdk.DEFAULT_HOST, default_host)

    def test_set_default_host_none(self):
        default_host = HttpSdk.DEFAULT_HOST
        HttpSdk.set_default_host(None)
        self.assertEqual(HttpSdk.DEFAULT_HOST, default_host)

    def test_set_default_proxy_without_scheme(self):
        default_proxy = HttpSdk.DEFAULT_PROXY
        HttpSdk.set_default_proxy("localhost:1234")
        self.assertEqual(HttpSdk.DEFAULT_PROXY, "http://localhost:1234")
        HttpSdk.set_default_proxy(default_proxy)
        self.assertEqual(HttpSdk.DEFAULT_PROXY, default_proxy)

    def test_incognito_mode_false_by_default(self):
        my_class = HttpSdk()
        self.assertFalse(my_class.incognito_mode)

    def test_incognito_mode_as_class_attribute(self):
        self.assertTrue(self.my_incognito_class.incognito_mode)
