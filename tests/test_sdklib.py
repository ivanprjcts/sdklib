# -*- coding: utf-8 -*-

import unittest
import pytest
import time
from sdklib.compat import bytes, is_py2, is_py3, exceptions
from sdklib.util.files import guess_filename_stream

from tests.sample_sdk import SampleHttpSdk


class TestSampleSdk(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # SampleHttpSdk.set_default_proxy("http://localhost:8080")
        cls.api = SampleHttpSdk()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_items(self):
        response = self.api.get_items()
        #self.assertEqual(response.status, 200)
        #self.assertTrue(isinstance(response.data, list))

    @pytest.mark.skipif(is_py2, reason="Cache not available in python 2.")
    def test_get_items_with_cache_py3(self):
        begin_timestamp = time.time()
        response = self.api.get_items_with_cache()
        elapsed_time = time.time() - begin_timestamp
        self.assertEqual(404, response.status)
        #self.assertTrue(isinstance(response.data, list))
        self.assertGreater(elapsed_time, 8)

        begin_timestamp = time.time()
        response = self.api.get_items_with_cache()
        elapsed_time = time.time() - begin_timestamp
        self.assertEqual(404, response.status)
        #self.assertTrue(isinstance(response.data, list))
        self.assertLess(elapsed_time, 8)

    @pytest.mark.skipif(is_py3, reason="Cache decorator raises exception in python 2.")
    def test_get_items_with_cache_py2(self):
        with self.assertRaises(exceptions.NotImplementedError):
            self.api.get_items_with_cache()

    def test_get_items_with_empty_query_params_parameter(self):
        response = self.api.get_items_with_empty_query_params_parameter()
        #self.assertEqual(response.status, 200)
        #self.assertTrue(isinstance(response.data, list))

    def test_create_item(self):
        response = self.api.create_item("mi nombre", "algo")
        self.assertEqual(404, response.status)

    def test_update_item(self):
        response = self.api.update_item(1, "mi nombre", "algo")
        self.assertEqual(404, response.status)

    def test_partial_update_item(self):
        response = self.api.partial_update_item(1, "mi nombre")
        self.assertEqual(404, response.status)

    def test_delete_item(self):
        response = self.api.delete_item(1)
        self.assertEqual(404, response.status)

    def test_login(self):
        response = self.api.login(username="user", password="password")
        self.assertEqual(404, response.status)

    def test_create_file(self):
        fname, fstream = guess_filename_stream("tests/resources/file.pdf")
        response = self.api.create_file_11paths_auth(fname, fstream, "235hWLEETQ46KWLnAg48",
                                                     "lBc4BSeqtGkidJZXictc3yiHbKBS87hjE078rswJ")
        self.assertEqual(404, response.status)

    def test_get_json_response(self):
        response = self.api.get_items()
        #self.assertEqual(response.status, 200)
        #self.assertTrue(isinstance(response.json, list))

    def test_get_raw_response(self):
        response = self.api.get_items()
        self.assertEqual(404, response.status, 200)
        self.assertTrue(isinstance(response.raw, bytes))
