import unittest

from sdklib.util.structures import get_dict_from_list, to_key_val_dict, to_key_val_list


class TestUtil(unittest.TestCase):

    def test_to_key_val_list(self):
        test_list = {'key1': 'val1', 'key0': 'val0'}
        res = to_key_val_list(test_list)
        self.assertTrue((res == [('key1', 'val1'), ('key0', 'val0')]) or (res == [('key0', 'val0'), ('key1', 'val1')]))

    def test_to_key_val_list_sorted(self):
        test_list = {'key1': 'val1', 'key0': 'val0'}
        res = to_key_val_list(test_list, sort=True)
        self.assertEqual(res, [('key0', 'val0'), ('key1', 'val1')])

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

