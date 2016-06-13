import unittest

from sdklib.http.renderers import FormRenderer
from sdklib.http.renderers import url_encode


class TestFormRender(unittest.TestCase):

    def test_encode_form_data_files(self):
        files = {"file_upload": "tests/resources/file.pdf", "file_upload2": "tests/resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = FormRenderer()
        body, content_type = r.encode_params(data, files=files)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=value2", body)
        self.assertIn("param1=value1", body)
        self.assertNotIn("file_upload", body)

    def test_encode_form_data_as_2tuple_parameter(self):
        data = [("param1", "value1"), ("param2", "value2"), ("param2", "value3")]

        r = FormRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertEqual(body, "param1=value1&param2=value2&param2=value3")

    def test_encode_form_data_no_data(self):
        r = FormRenderer()
        body, content_type = r.encode_params()
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertEqual(body, "")

    def test_encode_form_data_array_default(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=value2", body)
        self.assertIn("param1=value+1", body)
        self.assertIn("param2=value3", body)

    def test_encode_form_data_array_multi(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer(collection_format='multi')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=value2", body)
        self.assertIn("param1=value+1", body)
        self.assertIn("param2=value3", body)

    def test_encode_form_data_array_encoded(self):
        data = {"param1": "value 1", "param2": ["value2","value3"]}

        r = FormRenderer(collection_format='encoded')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=%5B%27value2%27%2C+%27value3%27%5D", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_array_csv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer(collection_format='csv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2[]=value2,value3", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_array_ssv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer(collection_format='ssv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2[]=value2 value3", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_array_tsv(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer(collection_format='tsv')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2[]=value2\tvalue3", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_array_pipes(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRenderer(collection_format='pipes')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2[]=value2|value3", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_boolean_false(self):
        data = {"param1": "value 1", "param2": False}

        r = FormRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=false", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_boolean_true(self):
        data = {"param1": "value 1", "param2": True}

        r = FormRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=true", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_none(self):
        data = {"param1": "value 1", "param2": None}

        r = FormRenderer()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=null", body)
        self.assertIn("param1=value+1", body)

    def test_encode_form_data_none_csharp(self):
        data = {"param1": "value 1", "param2": None}

        r = FormRenderer(output_str='csharp')
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=Null", body)
        self.assertIn("param1=value+1", body)

    def test_url_encode(self):
        params = {"param1": "value1", "param0": "value0"}
        value = url_encode(params, sort=True)
        self.assertEqual("param0=value0&param1=value1", value)
