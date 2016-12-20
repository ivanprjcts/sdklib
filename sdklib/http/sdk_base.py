import urllib3

from sdklib.http.renderers import JSONRenderer, MultiPartRenderer, get_renderer
from sdklib.compat import urlencode
from sdklib.util.parser import parse_args
from sdklib.util.urls import (
    get_hostname_parameters_from_url, ensure_url_path_starts_with_slash, ensure_url_path_format_suffix_starts_with_dot
)
from sdklib.http.response import HttpResponse
from sdklib.http.methods import *
from sdklib.util.logger import log_print_request, log_print_response


def generate_url_path(url_path_format, prefix=None, format_suffix=None, allow_key_errors=True, **kwargs):
    prefix = prefix or ''
    suffix = ensure_url_path_format_suffix_starts_with_dot(format_suffix)
    while True:
        try:
            return ensure_url_path_starts_with_slash(prefix + url_path_format.format(**kwargs) + suffix)
        except KeyError as e:
            if not allow_key_errors:
                raise
            key = e.args[0]
            kwargs[key] = '{%s}' % key
            continue
        except:
            raise


class HttpRequestContext(object):
    """
    Context object used to save http request parameters.
    """

    fields_to_clear = [
        'method', 'url_path', 'body_params', 'query_params', 'files'
    ]

    def __init__(self, host=None, proxy=None, method=None, prefix_url_path=None, url_path=None, url_path_params=None,
                 url_path_format=None, headers=None, query_params=None, body_params=None, files=None, renderer=None,
                 authentication_instances=None, response_class=None, update_content_type=None, redirect=None):
        """

        :param host:
        :param proxy:
        :param method:
        :param prefix_url_path:
        :param url_path:
        :param url_path_params:
        :param url_path_format:
        :param headers:
        :param query_params:
        :param body_params:
        :param files:
        :param renderer:
        :param authentication_instances:
        :param response_class:
        :param update_content_type: (bool) Update headers before performing the request, adding the Content-Type value
            according to the rendered body. By default: True.
        :param redirect: redirect requests automatically. By default: False
        """
        self.host = host
        self.proxy = proxy
        self.method = method
        self.prefix_url_path = prefix_url_path
        self.url_path = url_path
        self.url_path_params = url_path_params
        self.url_path_format = url_path_format
        self.headers = headers
        self.query_params = query_params
        self.body_params = body_params
        self.files = files
        self.renderer = renderer
        self.authentication_instances = authentication_instances
        self.response_class = response_class
        self.update_content_type = update_content_type
        self.redirect = redirect

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value or dict()

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

    @property
    def url_path_params(self):
        return self._url_path_params

    @url_path_params.setter
    def url_path_params(self, value):
        self._url_path_params = value or dict()

    @property
    def authentication_instances(self):
        return self._authentication_instances

    @authentication_instances.setter
    def authentication_instances(self, value):
        self._authentication_instances = value or []

    @property
    def response_class(self):
        return self._response_class

    @response_class.setter
    def response_class(self, value):
        self._response_class = value or HttpResponse

    @property
    def update_content_type(self):
        return self._update_content_type

    @update_content_type.setter
    def update_content_type(self, value):
        self._update_content_type = value if value is False else True

    @property
    def redirect(self):
        return self._redirect

    @redirect.setter
    def redirect(self, value):
        self._redirect = value if value is True else False

    def clear(self, *args):
        """
        Set default values to **self.fields_to_clear**. In addition, it is possible to pass extra fields to clear.

        :param args: extra fields to clear.
        """
        for field in self.fields_to_clear + list(args):
            setattr(self, field, None)


class HttpSdk(object):
    """
    Http sdk class.
    """
    from sdklib.http.headers import (
        ACCEPT_HEADER_NAME, ACCEPT_ENCODING_HEADER_NAME, ACCEPT_LANGUAGE_HEADER_NAME,
        AUTHORIZATION_HEADER_NAME, CACHE_CONTROL_HEADER_NAME, CONNECTION_HEADER_NAME, CONTENT_LENGTH_HEADER_NAME,
        CONTENT_TYPE_HEADER_NAME, COOKIE_HEADER_NAME, PRAGMA_HEADER_NAME, REFERRER_HEADER_NAME, USER_AGENT_HEADER_NAME
    )

    DEFAULT_HOST = "http://127.0.0.1:80"
    DEFAULT_PROXY = None
    DEFAULT_RENDERER = JSONRenderer()

    LOGIN_URL_PATH = None

    prefix_url_path = ""
    url_path_params = {}
    url_path_format = None
    authentication_instances = ()
    response_class = HttpResponse

    def __init__(self, host=None, proxy=None, default_renderer=None):
        self.host = host or self.DEFAULT_HOST
        self.proxy = proxy or self.DEFAULT_PROXY
        self.default_renderer = default_renderer or self.DEFAULT_RENDERER
        self._cookie = None
        self.incognito_mode = False

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
        A string that will be automatically included at the beginning of the url generated for doing each http request.

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
        A string that will be used to tell each request must be sent through this proxy server.
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
        if self.cookie and self.cookie.as_cookie_header_value() and not self.incognito_mode:
            headers[self.COOKIE_HEADER_NAME] = self.cookie.as_cookie_header_value()
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
        """
        Default: "http://127.0.0.1:80"

        A string that will be automatically included at the beginning of the url generated for doing each http request.
        """
        if value is None:
            cls.DEFAULT_HOST = "http://127.0.0.1:80"
        else:
            scheme, host, port = get_hostname_parameters_from_url(value)
            cls.DEFAULT_HOST = "%s://%s:%s" % (scheme, host, port)

    @classmethod
    def set_default_proxy(cls, value):
        """
        Default: None (no proxy)

        A string that will be used to tell each request must be sent through this proxy server.
        Use the scheme://hostname:port form.
        If you need to use a proxy, you can configure individual requests with the proxies argument to any request
        method.
        """
        if value is None:
            cls.DEFAULT_PROXY = None
        else:
            scheme, host, port = get_hostname_parameters_from_url(value)
            cls.DEFAULT_PROXY = "%s://%s:%s" % (scheme, host, port)

    @staticmethod
    def http_request_from_context(context, **kwargs):
        """
        Method to do http requests from context.

        :param context: request context.
        """
        context.method = context.method.upper()
        assert context.method in ALLOWED_METHODS

        context.url_path = generate_url_path(context.url_path, prefix=context.prefix_url_path,
                                             format_suffix=context.url_path_format, **context.url_path_params)

        if context.body_params or context.files:
            body, content_type = context.renderer.encode_params(context.body_params, files=context.files)
            if context.update_content_type and HttpSdk.CONTENT_TYPE_HEADER_NAME not in context.headers:
                context.headers[HttpSdk.CONTENT_TYPE_HEADER_NAME] = content_type
        else:
            body = None

        authentication_instances = context.authentication_instances
        for auth_obj in authentication_instances:
            context = auth_obj.apply_authentication(context)

        url = "%s%s" % (context.host, context.url_path)
        if context.query_params is not None:
            url += "?%s" % (urlencode(context.query_params))

        log_print_request(context.method, url, context.query_params, context.headers, body)
        r = HttpSdk.get_pool_manager(context.proxy).request(context.method,
                                                            url,
                                                            body=body,
                                                            headers=context.headers,
                                                            redirect=context.redirect)
        log_print_response(r.status, r.data, r.headers)
        r = context.response_class(r)
        return r

    def _http_request(self, method, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
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
        :param update_content_type: (bool) Update headers before performig the request, adding the Content-Type value
            according to the rendered body. By default: True.
        :return:
        """
        host = kwargs.get('host', self.host)
        proxy = kwargs.get('proxy', self.proxy)
        renderer = kwargs.get('renderer', MultiPartRenderer() if files else self.default_renderer)
        prefix_url_path = kwargs.get('prefix_url_path', self.prefix_url_path)
        authentication_instances = kwargs.get('authentication_instances', self.authentication_instances)
        url_path_format = kwargs.get('url_path_format', self.url_path_format)
        update_content_type = kwargs.get('update_content_type', True)
        redirect = kwargs.get('redirect', False)

        if headers is None:
            headers = self.default_headers()

        context = HttpRequestContext(
            host=host, proxy=proxy, method=method,
            prefix_url_path=prefix_url_path,
            url_path=url_path,
            url_path_params=self.url_path_params,
            url_path_format=url_path_format,
            headers=headers,
            query_params=query_params,
            body_params=body_params,
            files=files,
            renderer=renderer,
            response_class=self.response_class,
            authentication_instances=authentication_instances,
            update_content_type=update_content_type,
            redirect=redirect
        )
        res = self.http_request_from_context(context)
        self.cookie = res.cookie
        return res

    def get(self, url_path, headers=None, query_params=None, **kwargs):
        return self._http_request(GET_METHOD, url_path, headers, query_params, None, None, **kwargs)

    def post(self, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
        return self._http_request(POST_METHOD, url_path, headers, query_params, body_params, files,
                                  **kwargs)

    def put(self, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
        return self._http_request(PUT_METHOD, url_path, headers, query_params, body_params, files,
                                  **kwargs)

    def patch(self, url_path, headers=None, query_params=None, body_params=None, files=None, **kwargs):
        return self._http_request(PATCH_METHOD, url_path, headers, query_params, body_params, files,
                                  **kwargs)

    def delete(self, url_path, headers=None, query_params=None, **kwargs):
        return self._http_request(DELETE_METHOD, url_path, headers, query_params, None, None, **kwargs)

    def login(self, **kwargs):
        """
        Login abstract method with default implementation.

        :param kwargs: parameters
        :return: SdkResponse
        """
        assert self.LOGIN_URL_PATH is not None

        render_name = kwargs.pop("render", "json")
        render = get_renderer(render_name)
        params = parse_args(**kwargs)
        return self.post(self.LOGIN_URL_PATH, body_params=params, render=render)
