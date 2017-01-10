import unittest

from sdklib.util.parser import parse_args_as_tuple_list, parse_params_as_tuple_list


class TestParser(unittest.TestCase):

    def test_parse_args_as_tuple_list(self):
        res = parse_args_as_tuple_list(param="value", number=1)
        self.assertIn(("param", "value"), res)
        self.assertIn(("number", 1), res)

    def test_parse_params_as_tuple_list(self):
        res = parse_params_as_tuple_list({"param": "value", "number": 1})
        self.assertIn(("param", "value"), res)
        self.assertIn(("number", 1), res)
