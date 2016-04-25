"""
Library for helping SDK implementations
Version 0.2
"""
import ssl
import sys
import json
import collections
import urllib3

from .compat import urlencode
from .util.urls import get_hostname_parameters_from_url, ensure_url_path_starts_with_slash
from .renderers import JSONRender, MultiPartRender


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

    def __init__(self, host='http://127.0.0.1:80/', proxy=None, default_render=JSONRender()):
        self.host = host
        self.proxy = proxy
        self.default_render = default_render

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
        host = kwargs.get('host', self.host)
        proxy = kwargs.get('proxy', self.proxy)
        render = kwargs.get('render', self.default_render)

        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'TRACE', 'CONNECT']

        url_path = ensure_url_path_starts_with_slash(url_path)

        url = "%s%s" % (host, url_path)
        if query_params is not None:
            url += "?%s" % (urlencode(query_params))

        if files:
            render = MultiPartRender()

        body, content_type = render.encode_params(body_params, files=files)

        if headers is None:
            headers = self.default_headers()
            headers[self.CONTENT_TYPE_HEADER_NAME] = content_type

        r = self.pool_manager.request(method, url,
                                      fields=body,
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
