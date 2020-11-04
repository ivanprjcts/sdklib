import unittest

from sdklib.http.renderers import MultiPartRenderer
from sdklib.util.files import guess_filename_stream


class TestMultiPartRender(unittest.TestCase):

    def test_encode_multipart_data_files(self):
        files = {"file_upload": "tests/resources/file.pdf", "file_upload2": "tests/resources/file.png"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)
        self.assertIn(b"file_upload2", body)
        self.assertIn(b"file.png", body)
        self.assertIn(b"Content-Type: image/png", body)

    def test_encode_multipart_data_as_2tuple_files(self):
        files = {"file_upload": "tests/resources/file.pdf", "file_upload2": "tests/resources/file.png"}
        data = {"param1": ("value1", "myContentType"), "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(
            b'------------ThIs_Is_tHe_bouNdaRY\r\nContent-Disposition: form-data; name="param1"\r\nContent-Type: myContentType\r\n\r\nvalue1\r\n',
            body)
        self.assertIn(
            b'------------ThIs_Is_tHe_bouNdaRY\r\nContent-Disposition: form-data; name="param2"\r\n\r\nvalue2\r\n',
            body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)
        self.assertIn(b"file_upload2", body)
        self.assertIn(b"file.png", body)
        self.assertIn(b"Content-Type: image/png", body)

    def test_encode_multipart_data_files_as_2tuple_parameter(self):
        filename, stream = guess_filename_stream("tests/resources/file.pdf")
        filename2, stream2 = guess_filename_stream("tests/resources/file.png")
        files = {"file_upload1": (filename, stream), "file_upload2": (filename2, stream2)}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertNotIn(b"application/pdf", body)
        self.assertIn(b"file_upload2", body)
        self.assertIn(b"file.png", body)
        self.assertNotIn(b"Content-Type: image/png", body)

    def test_encode_multipart_data_files_as_3tuple_parameter(self):
        filename, stream = guess_filename_stream("tests/resources/file.pdf")
        files = {"file_upload1": (filename, stream, "application/xxx")}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/xxx", body)

    def test_encode_multipart_data_files_as_4tuple_parameter(self):
        filename, stream = guess_filename_stream("tests/resources/file.pdf")
        files = {"file_upload1": (filename, stream, "application/xxx", {"x-header": "value", "time": "now"})}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/xxx", body)
        self.assertIn(b"x-header: value", body)
        self.assertIn(b"time: now", body)

    def test_encode_multipart_data_and_no_files(self):
        files = {"file_upload": "tests/resources/file.pdf"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(None, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

    def test_encode_multipart_no_data_and_files(self):
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, None)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)

    def test_encode_multipart_data_files_using_boundary_as_init_parameter(self):
        files = {"file_upload": "tests/resources/file.pdf"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer("custom_boundary")
        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_using_boundary_as_parameter(self):
        files = {"file_upload": "tests/resources/file.pdf"}
        data = {"param1": "value1", "param2": "value2"}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"value2", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_boolean(self):
        files = {"file_upload": "tests/resources/file.pdf"}
        data = {"param1": "value1", "param2": True}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"true", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"true", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_none(self):
        files = {"file_upload": "tests/resources/file.pdf"}
        data = {"param1": "value1", "param2": None}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary")
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"null", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

        body, content_type = r.encode_params(data, files)
        self.assertEqual(content_type, "multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"null", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)

    def test_encode_multipart_data_files_none_csharp(self):
        files = {"file_upload": "tests/resources/file.pdf"}
        data = {"param1": "value1", "param2": None}

        r = MultiPartRenderer()
        body, content_type = r.encode_params(data, files, boundary="custom_boundary", output_str='csharp')
        self.assertEqual(content_type, "multipart/form-data; boundary=custom_boundary")
        self.assertIn(b"param1", body)
        self.assertIn(b"value1", body)
        self.assertIn(b"param2", body)
        self.assertIn(b"Null", body)
        self.assertIn(b"file_upload", body)
        self.assertIn(b"file.pdf", body)
        self.assertIn(b"Content-Type: application/pdf", body)
