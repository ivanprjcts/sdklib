import unittest

from sdklib.http import request_from_context, HttpRequestContext
from sdklib.http.session import Cookie


class TestRequestFromContext(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_create_item_from_context(self):
        context = HttpRequestContext(
            host="https://www.google.com",
            url_path="/items/",
            method="POST",
            body_params={"name": "mi nombre", "description": "algo"}
        )
        response = request_from_context(context=context)
        self.assertEqual(response.status, 404)

    def test_create_item_from_context_with_cookie(self):
        c = Cookie({"Set-Cookie": "new_param=marcos; another_new=ivan"})
        context = HttpRequestContext(
            host="https://www.google.com",
            url_path="/items/",
            method="POST",
            body_params={"name": "mi nombre", "description": "algo"},
            cookie=c
        )
        response = request_from_context(context=context)
        self.assertEqual(response.status, 404)
