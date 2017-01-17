import unittest

from sdklib.compat import cookies
from sdklib.http.session import Cookie


class TestSession(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cookie = Cookie({"Set-Cookie": "username=John Smith; expires=Thu, 18 Dec 2013 12:00:00 UTC; path=/"})

    def test_as_cookie_header_value(self):
        res = self.cookie.as_cookie_header_value()
        self.assertEqual(res, "username=John")

    def test_as_cookie_header_value_none(self):
        cookie = Cookie(None)
        res = cookie.as_cookie_header_value()
        self.assertEqual(res, "")

    def test_get_cookie_morsel(self):
        res = self.cookie.get("username")
        self.assertEqual(res.value, "John")

    def test_get_cookie(self):
        res = self.cookie.getcookie()
        self.assertTrue(isinstance(res, cookies.SimpleCookie))
