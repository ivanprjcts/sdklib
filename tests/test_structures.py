import unittest

from sdklib.util.structures import get_dict_from_list, to_key_val_dict, to_key_val_list, CaseInsensitiveDict


class TestStructures(unittest.TestCase):

    def test_to_key_val_list(self):
        test_list = {'key1': 'val1', 'key0': 'val0'}
        res = to_key_val_list(test_list)
        self.assertTrue((res == [('key1', 'val1'), ('key0', 'val0')]) or (res == [('key0', 'val0'), ('key1', 'val1')]))

    def test_to_key_val_list_sorted_insensitive(self):
        test_list = {'Key1': 'val1', 'key0': 'val0'}
        res = to_key_val_list(test_list, sort=True, insensitive=True)
        self.assertEqual(res, [('key0', 'val0'), ('Key1', 'val1')])

    def test_to_key_val_list_sorted_sensitive(self):
        test_list = {'Key1': 'val1', 'key0': 'val0'}
        res = to_key_val_list(test_list, sort=True, insensitive=False)
        self.assertEqual(res, [('Key1', 'val1'), ('key0', 'val0')])

    def test_to_key_val_list_none(self):
        res = to_key_val_list(None)
        self.assertIsNone(res)

    def test_to_key_val_list_exception(self):
        try:
            to_key_val_list(1)
            self.assertTrue(False)
        except ValueError:
            pass

    def test_get_dict_from_list(self):
        test_list = [{"Id": 0, "key2": "", "key3": ""},{"Id": 1, "key2": ""}, {"Id": 2, "key2": "", "key7": 4}]
        res = get_dict_from_list(test_list, Id=1)
        self.assertEqual(res, {"Id": 1, "key2": ""})

    def test_to_key_val_dict_json(self):
        json_obj = {"Id": 0, "key2": "", "key3": ""}
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": "", "key3": ""})

    def test_to_key_val_dict_tuple_list(self):
        json_obj = [("Id", 0), ("key2", ""), ("key3", "")]
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": "", "key3": ""})

    def test_to_key_val_dict_tuple_list_array(self):
        json_obj = [("Id", 0), ("key2", ""), ("key2", "val")]
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": ["", "val"]})

    def test_to_key_val_dict_tuple_list_double_array(self):
        json_obj = [("Id", 0), ("key2", [""]), ("key2", ["val", "val2"])]
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": ["", "val", "val2"]})

    def test_to_key_val_dict_tuple_list_array_append(self):
        json_obj = [("Id", 0), ("key2", [""]), ("key2", "val")]
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": ["", "val"]})

    def test_to_key_val_dict_tuple_list_three_elements(self):
        json_obj = [("Id", 0), ("key2", ""), ("key2", "val"), ("key2", "val2")]
        res = to_key_val_dict(json_obj)
        self.assertEqual(res, {"Id": 0, "key2": ["", "val", "val2"]})

    def test_to_key_val_dict_none(self):
        res = to_key_val_dict(None)
        self.assertEqual(res, {})

    def test_to_key_val_dict_exception(self):
        try:
            to_key_val_dict(1)
            self.assertTrue(False)
        except ValueError:
            pass

    def test_to_key_val_dict_invalid_array_of_dicts(self):
        try:
            to_key_val_dict([{"a": 1}, {"b": 2}])
            self.assertTrue(False)
        except ValueError:
            pass

    def test_to_key_val_dict_invalid_number_of_items(self):
        try:
            to_key_val_dict([(1, 2, 3), (1, 2, 3)])
            self.assertTrue(False)
        except ValueError:
            pass

    def test_case_insensitive_dict_basic_key_value_name(self):
        d = CaseInsensitiveDict({"X-key": "X-value"})
        self.assertEqual(1, len(d))
        self.assertEqual("X-key", list(d.keys())[0])
        self.assertEqual("X-value", list(d.values())[0])
        self.assertEqual("X-value", d["x-key"])

    def test_case_insensitive_dict_key_value_name_duplicated_keys(self):
        d = CaseInsensitiveDict({"X-key": "X-value", "x-key": "x-value"})
        self.assertEqual(1, len(d))
        self.assertEqual("X-key".lower(), list(d.keys())[0].lower())

    def test_case_insensitive_dict_key_value_update(self):
        d = CaseInsensitiveDict({"X-key": "X-value"})
        d["x-key"] = "x-value"
        self.assertEqual(1, len(d))
        self.assertEqual("x-key", list(d.keys())[0])
        self.assertEqual("x-value", list(d.values())[0])
        self.assertEqual("x-value", d["x-key"])
