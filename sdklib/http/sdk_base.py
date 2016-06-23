import urllib3

from sdklib.http.renderers import JSONRenderer, MultiPartRenderer, get_renderer
from sdklib.compat import urlencode
from sdklib.util.parser import parse_args
from sdklib.util.urls import get_hostname_parameters_from_url, ensure_url_path_starts_with_slash
from sdklib.http.response import HttpResponse
from sdklib.http.methods import *
from sdklib.http.headers import *


class HttpRequestContext(object):

    def __init__(self, host=None, proxy=None, method=None, url_path=None, headers=None, query_params=None,
                 body_params=None, files=None, renderer=None, authentication_instances=[]):
        self.host = host
        self.proxy = proxy
        self.method = method
        self.url_path = url_path
        self.headers = headers
        self.query_params = query_params
        self.body_params = body_params
        self.files = files
        self.renderer = renderer
        self.authentication_instances = authentication_instances

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value or dict()

    @property
    def renderer(self):
        return self._renderer

    @renderer.setter
    def renderer(self, value):
        self._renderer = value or JSONRenderer()

    @property
    def url_path(self):
        return self._url_path

    @url_path.setter
    def url_path(self, value):
        self._url_path = value or '/'

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, value):
        self._method = value or GET_METHOD


class HttpSdk(object):
    """
    Http sdk class.
    """
    DEFAULT_HOST = "http://127.0.0.1:80/"
    DEFAULT_PROXY = None
    DEFAULT_RENDERER = JSONRenderer()

    LOGIN_URL_PATH = None

    authentication_classes = ()

    def __init__(self, host=None, proxy=None, default_renderer=None):
        self.host = host or self.DEFAULT_HOST
        self.proxy = proxy or self.DEFAULT_PROXY
        self.default_renderer = default_renderer or self.DEFAULT_RENDERER
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
        headers[ACCEPT_HEADER_NAME] = "*/*"
        if self.cookie and self.cookie.as_cookie_header_value():
            headers[COOKIE_HEADER_NAME] = self.cookie.as_cookie_header_value()
        return headers

    @staticmethod
    def get_pool_manager(proxy=None):
        if proxy is not None:
            pm = urllib3.ProxyManager(
                proxy,
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

    @staticmethod
    def http_request_from_context(context):
        """
        Method to do http requests from context.
        """
        context.method = context.method.upper()
        assert context.method in ALLOWED_METHODS

        context.url_path = ensure_url_path_starts_with_slash(context.url_path)

        if context.body_params or context.files:
            body, content_type = context.renderer.encode_params(context.body_params, files=context.files)
            context.headers[CONTENT_TYPE_HEADER_NAME] = content_type
        else:
            body=None

        authentication_instances = context.authentication_instances
        for auth_obj in authentication_instances:
            context = auth_obj.apply_authentication(context)

        url = "%s%s" % (context.host, context.url_path)
        if context.query_params is not None:
            url += "?%s" % (urlencode(context.query_params))

        r = HttpSdk.get_pool_manager(context.proxy).request(context.method, url, body=body, headers=context.headers,
                                                            redirect=False)
        r = HttpResponse(r)
        return r

    def http_request(self, method, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
        """
        Method to do http requests.
        :param method:
        :param url_path:
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
        renderer = kwargs.get('renderer', MultiPartRenderer() if files else self.default_renderer)

        if headers is None:
            headers = self.default_headers()

        context = HttpRequestContext(host=host, proxy=proxy, method=method, url_path=url_path, headers=headers,
                                     query_params=query_params, body_params=body_params, files=files, renderer=renderer)
        res = self.http_request_from_context(context)
        self.cookie = res.cookie
        return res

    def login(self, **kwargs):
        """
        Basic Authentication method.
        :param kwargs: parameters
        :return: SdkResponse
        """
        assert self.LOGIN_URL_PATH is not None

        render_name = kwargs.pop("render", "json")
        render = get_renderer(render_name)
        params = parse_args(**kwargs)
        return self.http_request('POST', self.LOGIN_URL_PATH, body_params=params, render=render)
