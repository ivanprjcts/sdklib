# -*- coding: utf-8 -*-

import unittest

from sdklib.http.renderers import JSONRenderer


class TestJSONRender(unittest.TestCase):

    def test_encode_json_data_files(self):
        files = {"file_upload": "resources/file.pdf", "file_upload2": "resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = JSONRenderer()
        body, content_type = r.encode_params(data, files=files)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": "value2"', body)
        self.assertIn('"param1": "value1"', body)
        self.assertNotIn("file_upload", body)

    def test_encode_json_data_as_2tuple_parameter(self):
        data = [("param1", "value 1"), ("param2", "value2"), ("param2", "value3")]

        r = JSONRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": ["value2", "value3"]', body)
        self.assertIn('"param1": "value 1"', body)

    def test_encode_json_no_data(self):
        r = JSONRenderer()
        body, content_type = r.encode_params()
        self.assertEqual(content_type, "application/json")
        self.assertEqual("", body)

    def test_encode_json_data_including_array(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = JSONRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": ["value2", "value3"]', body)
        self.assertIn('"param1": "value 1"', body)

    def test_encode_json_data_unicode(self):
        data = {"param1": u"العَرَبِ", "param2": [u"válue", "value3"]}

        r = JSONRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": ["v\\u00e1lue", "value3"]', body)
        self.assertIn('"param1": "\\u0627\\u0644\\u0639\\u064e\\u0631\\u064e\\u0628\\u0650"', body)

    def test_encode_json_data_boolean(self):
        data = {"param1": "value 1", "param2": False}

        r = JSONRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": false', body)
        self.assertIn('"param1": "value 1"', body)

    def test_encode_json_data_none(self):
        data = {"param1": "value 1", "param2": None}

        r = JSONRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/json")
        self.assertIn('"param2": null', body)
        self.assertIn('"param1": "value 1"', body)
