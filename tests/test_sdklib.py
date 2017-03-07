# -*- coding: utf-8 -*-

import unittest
from sdklib.compat import bytes
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
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_get_items_with_empty_query_params_parameter(self):
        response = self.api.get_items_with_empty_query_params_parameter()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.data, list))

    def test_create_item(self):
        response = self.api.create_item("mi nombre", "algo")
        self.assertEqual(response.status, 201)

    def test_update_item(self):
        response = self.api.update_item(1, "mi nombre", "algo")
        self.assertEqual(response.status, 200)

    def test_partial_update_item(self):
        response = self.api.partial_update_item(1, "mi nombre")
        self.assertEqual(response.status, 405)

    def test_delete_item(self):
        response = self.api.delete_item(1)
        self.assertEqual(response.status, 204)

    def test_login(self):
        response = self.api.login(username="user", password="password")
        self.assertEqual(response.status, 404)

    def test_create_file(self):
        fname, fstream = guess_filename_stream("tests/resources/file.pdf")
        response = self.api.create_file_11paths_auth(fname, fstream, "235hWLEETQ46KWLnAg48",
                                                     "lBc4BSeqtGkidJZXictc3yiHbKBS87hjE078rswJ")
        self.assertEqual(response.status, 404)

    def test_get_json_response(self):
        response = self.api.get_items()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.json, list))

    def test_get_raw_response(self):
        response = self.api.get_items()
        self.assertEqual(response.status, 200)
        self.assertTrue(isinstance(response.raw, bytes))
