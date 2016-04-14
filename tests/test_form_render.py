import unittest

from sdklib.renderers import FormRender


class TestFormRender(unittest.TestCase):

    def test_form_data_files(self):
        files = {"file_upload": "resources/file.pdf", "file_upload2": "resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = FormRender()
        body, content_type = r.encode_params(data, files=files)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=value2", body)
        self.assertIn("param1=value1", body)
        self.assertNotIn("file_upload", body)

    def test_encode_multipart_data_as_2tuple_parameter(self):
        data = [("param1", "value1"), ("param2", "value2"), ("param2", "value3")]

        r = FormRender()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertEqual(body, "param1=value1&param2=value2&param2=value3")

    def test_encode_multipart_no_data(self):
        r = FormRender()
        body, content_type = r.encode_params()
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertEqual(body, "")

    def test_form_data_array_default(self):
        data = {"param1": "value 1", "param2": ["value2", "value3"]}

        r = FormRender()
        body, content_type = r.encode_params(data)
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        self.assertIn("param2=value2", body)
        self.assertIn("param1=value+1", body)
        self.assertIn("param2=value3", body)
