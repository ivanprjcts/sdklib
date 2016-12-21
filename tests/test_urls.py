import unittest

from sdklib.util.urls import (
    get_hostname_parameters_from_url, urlsplit, ensure_url_path_starts_with_slash, generate_url
)
from sdklib.http import generate_url_path


class TestUrls(unittest.TestCase):

    def test_get_hostname_parameters_from_url_with_http_schema(self):
        scheme, host, port,  = get_hostname_parameters_from_url("http://myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '80')

    def test_get_hostname_parameters_from_url_with_subdomain(self):
        scheme, host, port = get_hostname_parameters_from_url("https://cybersecurity-telefonica.e-paths.com")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'cybersecurity-telefonica.e-paths.com')
        self.assertEqual(port, '443')

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
        scheme, host, port, _, _ = urlsplit("http://myhost.com/")
        self.assertEqual(scheme, 'http')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_empty_schema(self):
        scheme, host, port, _, _ = urlsplit("://myhost.com/")
        self.assertEqual(scheme, '')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_https_schema(self):
        scheme, host, port, _, _ = urlsplit("https://myhost.com/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_https_and_port(self):
        scheme, host, port, _, _ = urlsplit("https://myhost.com:66/")
        self.assertEqual(scheme, 'https')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '66')

    def test_urlsplit_without_schema(self):
        scheme, host, port, _, _ = urlsplit("myhost.com/")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_without_end_slash(self):
        scheme, host, port, _, _ = urlsplit("myhost.com")
        self.assertEqual(scheme, None)
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_with_non_http_schema(self):
        scheme, host, port, _, _ = urlsplit("ftp://myhost.com")
        self.assertEqual(scheme, 'ftp')
        self.assertEqual(host, 'myhost.com')
        self.assertEqual(port, '')

    def test_urlsplit_localhost(self):
        scheme, host, port, _, _ = urlsplit("http://localhost:8080")
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

    def test_generate_url_path_without_prefix(self):
        url_path = generate_url_path("/path/to/{id}/", id=1)
        self.assertEqual("/path/to/1/", url_path)

    def test_generate_url_path_with_prefix(self):
        url_path = generate_url_path("/path/to/{id}/", prefix="/example", id=1)
        self.assertEqual("/example/path/to/1/", url_path)

    def test_generate_url_path_with_multiple_params(self):
        url_path = generate_url_path("/path/to/{id}/{lang}/", id=1, lang='es')
        self.assertEqual("/path/to/1/es/", url_path)

    def test_generate_url_path_extra_param(self):
        url_path = generate_url_path("/path/to/{lang}/", lang='es', invented='hello')
        self.assertEqual("/path/to/es/", url_path)

    def test_generate_url_path_missing_param(self):
        url_path = generate_url_path("/path/to/{id}/{lang}/", lang='es')
        self.assertEqual("/path/to/{id}/es/", url_path)

    def test_generate_url_path_multiples_missing_param(self):
        url_path = generate_url_path("/path/to/{id}/{lang}/{format}/", lang='es')
        self.assertEqual("/path/to/{id}/es/{format}/", url_path)

    def test_generate_url_path_format_suffix(self):
        url_path = generate_url_path("/path/to/{id}/{lang}/{format}/", format_suffix='json', lang='es')
        self.assertEqual("/path/to/{id}/es/{format}/.json", url_path)

    def test_generate_url_full(self):
        url = generate_url(scheme="http", host="myhost.com", port=80, path="path", query={"param": "value"})
        self.assertEqual("http://myhost.com:80/path?param=value", url)

    def test_generate_url_scheme_host_port_and_path(self):
        url = generate_url(scheme="http", host="myhost.com", port=80, path="path")
        self.assertEqual("http://myhost.com:80/path", url)

    def test_generate_url_scheme_host_and_path(self):
        url = generate_url(scheme="http", host="myhost.com", path="path")
        self.assertEqual("http://myhost.com/path", url)

    def test_generate_url_scheme_and_host(self):
        url = generate_url(scheme="http", host="myhost.com")
        self.assertEqual("http://myhost.com", url)
