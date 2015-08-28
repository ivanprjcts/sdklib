import unittest

from sdklib.util.dictionay import get_dict_from_list


class TestUtil(unittest.TestCase):

    def test_get_dict_from_list(self):
        test_list = [{"Id": 0, "key2": "", "key3": ""},{"Id": 1, "key2": ""}, {"Id": 2, "key2": "", "key7": 4}]
        res = get_dict_from_list(test_list, Id=1)

        self.assertEqual(res, {"Id": 1, "key2": ""})


if __name__ == '__main__':
    unittest.main()