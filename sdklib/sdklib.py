"""
Library for helping SDK implementations
Version 0.2
"""
import ssl
import sys
import json
import collections
import urllib3

try:
    from urllib.parse import urlencode
except:
    from urllib import urlencode


from .util.urls import get_hostname_parameters_from_url, ensure_url_path_starts_with_slash
from .util.file import guess_filename_stream
from .util.parser import parse_params_as_tuple_list


class SdkResponse(object):

    def __init__(self, data):
        try:
            self.data = json.loads(data)
        except ValueError:
            self.data = data

    def get_data(self):
        return self.data


class SdkBase(object):
    """
    Sdk Base.
    """
    USER_AGENT_HEADER_NAME = "User-Agent"
    PRAGMA_HEADER_NAME = "Pragma"
    CONTENT_TYPE_HEADER_NAME = "Content-Type"
    CONTENT_LENGTH_HEADER_NAME = "Content-Length"
    ACCEPT_HEADER_NAME = "Accept"
    ACCEPT_LANGUAGE_HEADER_NAME = "Accept-Language"
    ACCEPT_ENCODING_HEADER_NAME = "Accept-Encoding"
    CACHE_CONTROL_HEADER_NAME = "Cache-Control"
    CONNECTION_HEADER_NAME = "Connection"
    REFERRER_HEADER_NAME = "Referer"

    CONTENT_TYPE_JSON = "application/json"
    CONTENT_TYPE_URL_ENCODED = "application/x-www-form-urlencoded"
    CONTENT_TYPE_OCTET = "application/octet-stream"
    CONTENT_TYPE_PLAIN_TEXT = "text/plain; charset=utf-8"
    CONTENT_TYPE_MULTIPART_FORM_DATA = "multipart/form-data"

    BOUNDARY = "----------ThIs_Is_tHe_bouNdaRY_$"

    def __init__(self):
        self.host = "http://127.0.0.1:80/"
        self.proxy = None

    @property
    def host(self):
        """
        Get hostname.
        :return: host value
        """
        return self._host

    @host.setter
    def host(self, value):
        """
        Set hostname.
        :param value: The host to be connected with, e.g. (http://hostname) or (https://X.X.X.X:port)
        """
        scheme, host, port = get_hostname_parameters_from_url(value)
        self._host = "%s://%s:%s" % (scheme, host, port)

    @property
    def proxy(self):
        """
        Get proxy url.
        :return: proxy url value
        """
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        """
        Set proxy.
        :param value:
        """
        self._proxy = value

    @staticmethod
    def encode_multipart_formdata(fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + SdkBase.BOUNDARY)
            L.append('Content-Disposition: form-data; name=%s' % key)
            L.append('Content-Type: %s' % SdkBase.CONTENT_TYPE_JSON)
            L.append('')
            L.append(str(value))
        for (key, value) in files:
            filename, stream = guess_filename_stream(value)
            L.append('--' + SdkBase.BOUNDARY)
            L.append('Content-Disposition: form-data; name=%s; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % SdkBase.CONTENT_TYPE_OCTET)
            L.append('')
            L.append(stream)
        L.append('--' + SdkBase.BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        return body

    def default_headers(self):
        return dict()

    def _http_request(self, method, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
        """
        Internal method to do http requests.
        :param method:
        :param url:
        :param headers:
        :param body_params:
        :param query_params:
        :param files: (optional) Dictionary of ``'name': file-like-objects`` (or ``{'name': file-tuple}``) for multipart
            encoding upload.
            ``file-tuple`` can be a 1-tuple ``('filepath')``, 2-tuple ``('filepath', 'content_type')``
            or a 3-tuple ``('filepath', 'content_type', custom_headers)``, where ``'content-type'`` is a string
            defining the content type of the given file and ``custom_headers`` a dict-like object containing additional
            headers to add for the file.
        :return:
        """
        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'TRACE', 'CONNECT']

        url_path = ensure_url_path_starts_with_slash(url_path)

        url = "%s%s" % (self.host, url_path)
        if query_params is not None:
            url += "?%s" % (urlencode(query_params))

        if files:
            try:
                files = parse_params_as_tuple_list(files)
            except TypeError:
                pass
            try:
                fields = parse_params_as_tuple_list(body_params)
            except TypeError:
                fields = body_params
            body = self.encode_multipart_formdata(fields=fields, files=files)
            headers[self.CONTENT_TYPE_HEADER_NAME] = '%s; boundary=%s' % (self.CONTENT_TYPE_MULTIPART_FORM_DATA,
                                                                          self.BOUNDARY)
        elif form_urlencoding:
            if body_params is not None:
                parameters = urlencode(body_params)
            else:
                parameters = ""
            xHeaders[self.CONTENT_TYPE_HEADER_NAME] = self.CONTENT_TYPE_URL_ENCODED
        elif isinstance(body_params, collections.Mapping):
            try:
                parameters = json.dumps(body_params)
            except:
                parameters = json.dumps(body_params, encoding='latin-1')
            xHeaders[self.CONTENT_TYPE_HEADER_NAME] = self.CONTENT_TYPE_JSON
        else:
            parameters = body_params
            xHeaders[self.CONTENT_TYPE_HEADER_NAME] = self.CONTENT_TYPE_PLAIN_TEXT

        if headers is None:
            headers = self.default_headers()

        r = self.pool_manager.request(method, url,
                                      fields=body_params,
                                      encode_multipart=True,
                                      headers=headers)

        response = conn.getresponse()

        status = response.status
        res_headers = response.getheaders()
        read_data = response.read()
        try:
            res_data = read_data.decode('utf-8')
        except UnicodeDecodeError:
            res_data = read_data

        conn.close()

        return status, res_data, dict(res_headers)
