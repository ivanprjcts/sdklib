import unittest

from sdklib.util.urls import get_hostname_parameters_from_url, urlsplit, ensure_url_path_starts_with_slash


class TestUrls(unittest.TestCase):

    def test_get_hostname_parameters_from_url_with_http_schema(self):
        scheme, host, port = get_hostname_parameters_from_url("http://myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_get_hostname_parameters_from_url_with_empty_schema(self):
        scheme, host, port = get_hostname_parameters_from_url("://myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_get_hostname_parameters_from_url_with_https_schema(self):
        scheme, host, port = get_hostname_parameters_from_url("https://myhost.com/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '443')

    def test_get_hostname_parameters_from_url_https_and_port(self):
        scheme, host, port = get_hostname_parameters_from_url("https://myhost.com:66/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '66')

    def test_get_hostname_parameters_from_url_http_and_non_default_port(self):
        scheme, host, port = get_hostname_parameters_from_url("http://myhost.com:66/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '66')

    def test_get_hostname_parameters_from_url_without_schema(self):
        scheme, host, port = get_hostname_parameters_from_url("myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_get_hostname_parameters_from_url_without_end_slash_(self):
        scheme, host, port = get_hostname_parameters_from_url("myhost.com")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_get_hostname_parameters_from_url_with_non_http_schema(self):
        scheme, host, port = get_hostname_parameters_from_url("ftp://myhost.com")
        self.assertEqual(scheme, 'ftp')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_urlsplit_http_schema(self):
        scheme, host, port = urlsplit("http://myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_empty_schema(self):
        scheme, host, port = urlsplit("://myhost.com/")
        self.assertEqual(scheme, '')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_https_schema(self):
        scheme, host, port = urlsplit("https://myhost.com/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_https_and_port(self):
        scheme, host, port = urlsplit("https://myhost.com:66/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '66')

    def test_urlsplit_without_schema(self):
        scheme, host, port = urlsplit("myhost.com/")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_without_end_slash(self):
        scheme, host, port = urlsplit("myhost.com")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_with_non_http_schema(self):
        scheme, host, port = urlsplit("ftp://myhost.com")
        self.assertEqual(scheme, 'ftp')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_localhost(self):
        scheme, host, port = urlsplit("http://localhost:8080")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'localhost')
        self.assertEqual(port, '8080')

    def test_ensure_url_path_starts_with_slash_empty_string(self):
        url = ensure_url_path_starts_with_slash("")
        self.assertEqual(url, "/")

    def test_ensure_url_path_starts_with_slash_none(self):
        url = ensure_url_path_starts_with_slash(None)
        self.assertEqual(url, "/")

    def test_ensure_url_path_starts_with_slash_if_it_has_it(self):
        url = ensure_url_path_starts_with_slash("/api/1.0/")
        self.assertEqual(url, "/api/1.0/")

    def test_ensure_url_path_starts_with_slash_if_it_has_not_it(self):
        url = ensure_url_path_starts_with_slash("api/1.0/")
        self.assertEqual(url, "/api/1.0/")