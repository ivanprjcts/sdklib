# -*- coding: utf-8 -*-

import unittest

from sdklib.renderers import PlainTextRender


class TestPlainTextRender(unittest.TestCase):

    def test_encode_plain_data_files(self):
        files = {"file_upload": "resources/file.pdf", "file_upload2": "resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = PlainTextRender()
        body, content_type = r.encode_params(data, files=files)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn("param1=value1", body)
        self.assertIn("param2=value2", body)
        self.assertNotIn("file_upload", body)

    def test_encode_plain_data_as_2tuple_parameter(self):
        data = [("param1", "value 1"), ("param2", "value2"), ("param2", "value3")]

        r = PlainTextRender()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertEqual("param1=value 1\nparam2=value2\nparam2=value3", body)

    def test_encode_plain_no_data(self):
        r = PlainTextRender()
        body, content_type = r.encode_params()
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertEqual("", body)

    def test_encode_plain_data_charset_default(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRender()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn("param1=value 1", body)
        self.assertIn("param2=value2", body)
        self.assertIn("param2=value3", body)

    def test_encode_plain_data_charset_ascii(self):
        data = {"param1": "value 1", "param2": "value2"}

        r = PlainTextRender(charset='ascii')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=ascii")
        self.assertIn("param1=value 1", body)
        self.assertIn("param2=value2", body)

    def test_encode_plain_data_no_charset(self):
        data = {"param1": "value 1", "param2": "value2"}

        r = PlainTextRender(charset=None)
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain")
        self.assertIn("param1=value 1", body)
        self.assertIn("param2=value2", body)

    def test_encode_plain_data_unicode(self):
        data = u"Hello! I'm Iván Martín!"

        r = PlainTextRender(charset=None)
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain")
        self.assertEqual(u"Hello! I'm Iv\xe1n Mart\xedn!", body)
