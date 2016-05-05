import unittest

from sdklib.renderers import MultiPartRender
from sdklib.util.files import guess_filename_stream


class TestMultiPartRender(unittest.TestCase):

    def test_encode_multipart_data_files(self):
        files = {"file_upload": "resources/file.pdf", "file_upload2": "resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)
        self.assertIn("file_upload2", body)
        self.assertIn("file.png", body)
        self.assertIn("Content-Type: image/png", body)

    def test_encode_multipart_data_files_as_2tuple_parameter(self):
        filename, stream = guess_filename_stream("resources/file.pdf")
        filename2, stream2 = guess_filename_stream("resources/file.png")
        files = {"file_upload1": (filename, stream), "file_upload2": (filename2, stream2)}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertNotIn("application/pdf", body)
        self.assertIn("file_upload2", body)
        self.assertIn("file.png", body)
        self.assertNotIn("Content-Type: image/png", body)

    def test_encode_multipart_data_files_as_3tuple_parameter(self):
        filename, stream = guess_filename_stream("resources/file.pdf")
        files = {"file_upload1": (filename, stream, "application/xxx")}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/xxx", body)

    def test_encode_multipart_data_files_as_4tuple_parameter(self):
        filename, stream = guess_filename_stream("resources/file.pdf")
        files = {"file_upload1": (filename, stream, "application/xxx", {"x-header": "value", "time": "now"})}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/xxx", body)
        self.assertIn("x-header: value", body)
        self.assertIn("time: now", body)

    def test_encode_multipart_data_and_no_files(self):
        files = {"file_upload": "resources/file.pdf"}

        r = MultiPartRender()
        body, content_type = r.encode_params(None, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

    def test_encode_multipart_no_data_and_files(self):
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, None)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)

    def test_encode_multipart_data_files_using_boundary_as_init_parameter(self):
        files = {"file_upload": "resources/file.pdf"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender("custom_boundary")
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_using_boundary_as_parameter(self):
        files = {"file_upload": "resources/file.pdf"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("value2", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_boolean(self):
        files = {"file_upload": "resources/file.pdf"}
        data = {"param1": "value1", "param2": True}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("true", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("true", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_none(self):
        files = {"file_upload": "resources/file.pdf"}
        data = {"param1": "value1", "param2": None}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("null", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("null", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_none_csharp(self):
        files = {"file_upload": "resources/file.pdf"}
        data = {"param1": "value1", "param2": None}

        r = MultiPartRender()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary", output_str='csharp')
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn("param1", body)
        self.assertIn("value1", body)
        self.assertIn("param2", body)
        self.assertIn("Null", body)
        self.assertIn("file_upload", body)
        self.assertIn("file.pdf", body)
        self.assertIn("Content-Type: application/pdf", body)
