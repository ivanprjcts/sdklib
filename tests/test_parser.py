import unittest

from sdklib.util.parser import (
    parse_args_as_tuple_list, parse_params_as_tuple_list, safe_add_slash, safe_add_end_slash, get_url_query_params,
    parse_params
)


class TestParser(unittest.TestCase):

    def test_parse_args_as_tuple_list(self):
        res = parse_args_as_tuple_list(param="value", number=1)
        self.assertIn(("param", "value"), res)
        self.assertIn(("number", 1), res)

    def test_parse_args_as_tuple_list_with_array(self):
        res = parse_args_as_tuple_list(param="value", number=1, array=[1, 2, 3])
        self.assertIn(("param", "value"), res)
        self.assertIn(("number", 1), res)
        self.assertIn(("array", 1), res)

    def test_parse_params_as_tuple_list(self):
        res = parse_params_as_tuple_list({"param": "value", "number": 1})
        self.assertIn(("param", "value"), res)
        self.assertIn(("number", 1), res)

    def test_safe_add_slash(self):
        res = safe_add_slash("path/to/something")
        self.assertEqual("/path/to/something", res)

    def test_safe_add_slash_blank(self):
        res = safe_add_slash(None)
        self.assertEqual("", res)

    def test_safe_add_end_slash(self):
        res = safe_add_end_slash(None)
        self.assertEqual("", res)

    def test_get_url_query_params(self):
        res = get_url_query_params({"param": "value"})
        self.assertEqual("?param=value", res)

    def test_parse_params(self):
        res = parse_params({"param": "value", "param2": None})
        self.assertEqual({"param": "value"}, res)
