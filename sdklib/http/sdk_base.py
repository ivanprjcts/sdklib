import urllib3

from sdklib.http.renderers import JSONRender, MultiPartRender, get_render
from sdklib.compat import urlencode
from sdklib.util.parser import parse_args
from sdklib.util.urls import get_hostname_parameters_from_url, ensure_url_path_starts_with_slash
from sdklib.http.response import HttpResponse


class HttpSdk(object):
    """
    Http sdk class.
    """
    DEFAULT_HOST = "http://127.0.0.1:80/"
    DEFAULT_PROXY = None
    DEFAULT_RENDER = JSONRender()

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
    COOKIE_HEADER_NAME = "Cookie"
    X_CSRF_TOKEN_HEADER_NAME = "X-CSRFToken"

    LOGIN_URL_PATH = None

    def __init__(self, host=None, proxy=None, default_render=None):
        self.host = host or self.DEFAULT_HOST
        self.proxy = proxy or self.DEFAULT_PROXY
        self.default_render = default_render or self.DEFAULT_RENDER
        self._cookie = None

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

    @property
    def cookie(self):
        """
        Get cookie.
        :return: cookie value
        """
        return self._cookie

    @cookie.setter
    def cookie(self, value):
        """
        Set cookie.
        :param value:
        """
        if value and not value.is_empty():
            self._cookie = value

    def default_headers(self):
        headers = dict()
        headers[self.ACCEPT_HEADER_NAME] = "*/*"
        if self.cookie and self.cookie.as_cookie_header_value():
            headers[self.COOKIE_HEADER_NAME] = self.cookie.as_cookie_header_value()
        return headers

    @property
    def pool_manager(self):
        if self.proxy:
            pm = urllib3.ProxyManager(
                self.proxy,
                num_pools=10,
            )
        else:
            pm = urllib3.PoolManager(
                num_pools=10,
            )
        return pm

    @classmethod
    def set_default_host(cls, value):
        scheme, host, port = get_hostname_parameters_from_url(value)
        cls.DEFAULT_HOST = "%s://%s:%s" % (scheme, host, port)

    @classmethod
    def set_default_proxy(cls, value):
        cls.DEFAULT_PROXY = value

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
        render = kwargs.get('render', MultiPartRender() if files else self.default_render)

        method = method.upper()
        assert method in ['GET', 'HEAD', 'DELETE', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'TRACE', 'CONNECT']

        url_path = ensure_url_path_starts_with_slash(url_path)

        url = "%s%s" % (host, url_path)
        if query_params is not None:
            url += "?%s" % (urlencode(query_params))

        body, content_type = render.encode_params(body_params, files=files)

        if headers is None:
            headers = self.default_headers()
            headers[self.CONTENT_TYPE_HEADER_NAME] = content_type

        r = self.pool_manager.request(method, url, body=body, headers=headers, redirect=False)
        r = HttpResponse(r)
        self.cookie = r.cookie  # update cookie

        return r

    def login(self, **kwargs):
        """
        Basic Authentication method.
        :param kwargs: parameters
        :return: SdkResponse
        """
        assert self.LOGIN_URL_PATH is not None

        render_name = kwargs.pop("render", "json")
        render = get_render(render_name)
        params = parse_args(**kwargs)
        return self._http_request('POST', self.LOGIN_URL_PATH, body_params=params, render=render)
