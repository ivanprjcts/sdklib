# -*- coding: utf-8 -*-

import unittest

from sdklib.http.renderers import PlainTextRenderer


class TestPlainTextRender(unittest.TestCase):

    def test_encode_plain_data_files(self):
        files = {"file_upload": "tests/resources/file.pdf", "file_upload2": "tests/resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = PlainTextRenderer()
        body, content_type = r.encode_params(data, files=files)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value1", body)
        self.assertIn(b"param2=value2", body)
        self.assertNotIn(b"file_upload", body)

    def test_encode_plain_data_as_2tuple_parameter(self):
        data = [("param1", "value 1"), ("param2", "value2"), ("param2", "value3")]

        r = PlainTextRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertEqual(b"param1=value 1\nparam2=value2\nparam2=value3", body)

    def test_encode_plain_no_data(self):
        r = PlainTextRenderer()
        body, content_type = r.encode_params()
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertEqual("", body)

    def test_encode_plain_data_charset_default(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=value2", body)
        self.assertIn(b"param2=value3", body)

    def test_encode_plain_data_charset_ascii(self):
        data = {"param1": "value 1", "param2": "value2"}

        r = PlainTextRenderer(charset='ascii')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=ascii")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=value2", body)

    def test_encode_plain_data_no_charset(self):
        data = {"param1": "value 1", "param2": "value2"}

        r = PlainTextRenderer(charset=None)
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=value2", body)

    def test_encode_plain_data_unicode(self):
        data = u"Hello! I'm Iván Martín!"

        r = PlainTextRenderer(charset=None)
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain")
        self.assertEqual(u"Hello! I'm Iv\xe1n Mart\xedn!", body)

    def test_encode_plain_data_array_csv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer(collection_format='csv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2[]=value2,value3", body)

    def test_encode_plain_data_array_ssv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer(collection_format='ssv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2[]=value2 value3", body)

    def test_encode_plain_data_array_tsv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer(collection_format='tsv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2[]=value2\tvalue3", body)

    def test_encode_plain_data_array_pipes(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer(collection_format='pipes')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2[]=value2|value3", body)

    def test_encode_plain_data_array_plain(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = PlainTextRenderer(collection_format='plain')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=['value2', 'value3']", body)

    def test_encode_plain_data_boolean(self):
        data = {"param1": "value 1", "param2": False}

        r = PlainTextRenderer(collection_format='plain')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=false", body)

    def test_encode_plain_data_none(self):
        data = {"param1": "value 1", "param2": None}

        r = PlainTextRenderer(collection_format='plain')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=null", body)

    def test_encode_plain_data_none_csharp(self):
        data = {"param1": "value 1", "param2": None}

        r = PlainTextRenderer(collection_format='plain', output_str='csharp')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=Null", body)

    def test_encode_plain_data_true_csharp(self):
        data = {"param1": "value 1", "param2": True}

        r = PlainTextRenderer(collection_format='plain', output_str='csharp')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=True", body)

    def test_encode_plain_data_none_python(self):
        data = {"param1": "value 1", "param2": None}

        r = PlainTextRenderer(collection_format='plain', output_str='python')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=None", body)

    def test_encode_plain_data_true_python(self):
        data = {"param1": "value 1", "param2": True}

        r = PlainTextRenderer(collection_format='plain', output_str='python')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "text/plain; charset=utf-8")
        self.assertIn(b"param1=value 1", body)
        self.assertIn(b"param2=True", body)
