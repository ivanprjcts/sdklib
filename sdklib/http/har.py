import json
import copy
from sdklib.compat import str, unquote_plus
from sdklib import http
from sdklib.http import HttpRequestContext
from sdklib.http.renderers import get_renderer
from sdklib.http.response import Response as HttpResponse
from sdklib.util.urls import urlsplit


class Cookie(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def name(self):
        return self._dict.get("name", None)

    @property
    def value(self):
        return self._dict.get("value", None)

    @property
    def expires(self):
        return self._dict.get("expires", None)

    @property
    def http_only(self):
        return self._dict.get("httpOnly", None)

    @property
    def secure(self):
        return self._dict.get("secure", None)


class Request(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def method(self):
        return self._dict.get("method", None)

    @property
    def url(self):
        return self._dict.get("url", None)

    @property
    def http_version(self):
        return self._dict.get("httpVersion", None)

    @property
    def headers(self):
        headers = self._dict.get("headers", None)
        return {h["name"]: h["value"] for h in headers}

    @property
    def query_string(self):
        query_string = self._dict.get("queryString", None)
        return {unquote_plus(h["name"]): unquote_plus(h["value"]) for h in query_string}

    @property
    def post_data(self):
        post_data = self._dict.get("postData", {})
        params = {unquote_plus(h["name"]): unquote_plus(h["value"]) for h in post_data.get("params", [])}
        mime_type = post_data.get("mimeType", None)
        return params, get_renderer(mime_type=mime_type)

    @property
    def cookies(self):
        return [Cookie(c) for c in self._dict.get("cookies", [])]

    @property
    def headers_size(self):
        return self._dict.get("headersSize", None)

    @property
    def body_size(self):
        return self._dict.get("bodySize", None)

    def as_http_request_context(self):
        scheme, domain_or_ip, port, path, _ = urlsplit(self.url)
        host = scheme + "://" + domain_or_ip
        if port:
            host += ":" + str(port)
        body_params, renderer = self.post_data
        return HttpRequestContext(
            host=host, method=self.method, url_path=path, query_params=self.query_string, headers=self.headers,
            renderer=renderer, body_params=body_params
        )


class Content(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def size(self):
        return self._dict.get("size", None)

    @property
    def mime_type(self):
        return self._dict.get("mimeType", None)

    @property
    def compression(self):
        return self._dict.get("compression", None)

    @property
    def text(self):
        return self._dict.get("text", None)


class Response(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def status(self):
        return self._dict.get("status", None)

    @property
    def status_text(self):
        return self._dict.get("statusText", None)

    @property
    def http_version(self):
        return self._dict.get("httpVersion", None)

    @property
    def headers(self):
        headers = self._dict.get("headers", None)
        return {h["name"]: h["value"] for h in headers}

    @property
    def cookies(self):
        return [Cookie(c) for c in self._dict.get("cookies", [])]

    @property
    def redirect_url(self):
        return self._dict.get("redirectURL", None)

    @property
    def headers_size(self):
        return self._dict.get("headersSize", None)

    @property
    def body_size(self):
        return self._dict.get("bodySize", None)

    @property
    def transfer_size(self):
        return self._dict.get("_transferSize", None)

    @property
    def content(self):
        c = self._dict.get("content", None)
        return None if c is None else Content(c)

    def as_http_response(self):
        return HttpResponse(
            headers=self.headers, status_text=self.status_text, status=self.status, http_version=self.http_version,
            body=self.content.text
        )


class Entry(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def started_date_time(self):
        return self._dict.get("startedDateTime", None)

    @property
    def time(self):
        return self._dict.get("time", None)

    @property
    def request(self):
        r = self._dict.get("request", None)
        return None if r is None else Request(r)

    @property
    def response(self):
        r = self._dict.get("response", None)
        return None if r is None else Response(r)

    @property
    def cache(self):
        return self._dict.get("cache", None)

    @property
    def timings(self):
        return self._dict.get("timings", None)

    @property
    def server_ip_address(self):
        return self._dict.get("serverIPAddress", None)

    @property
    def connection(self):
        return self._dict.get("connection", None)

    @property
    def pageref(self):
        return self._dict.get("pageref", None)


class Log(object):

    def __init__(self, j):
        self._dict =json.loads(j) if isinstance(j, str) else j

    @property
    def version(self):
        return self._dict.get("version", None)

    @property
    def creator(self):
        return self._dict.get("creator", None)

    @property
    def pages(self):
        return self._dict.get("pages", None)

    @property
    def entries(self):
        return [Entry(e) for e in self._dict.get("entries", [])]


class HAR(object):

    def __init__(self, j):
        self._dict = json.loads(j)

    @property
    def log(self):
        l = self._dict.get("log", None)
        return None if l is None else Log(l)


def _find_value_in_new_response(value, prev_response_ctx, new_response_ctx):
    try:
        elem = prev_response_ctx.html.find_element_by_xpath("//*[@*='{}']".format(value))
        name = elem.get("name")

        new_elem = new_response_ctx.html.find_element_by_name(name)
        return new_elem.get("value")
    except:
        pass


def _update_dynamic_elements(prev_response_ctx, response_ctx, request_ctx):
    ctx = copy.deepcopy(request_ctx)
    if response_ctx is not None and not response_ctx.cookie.is_empty():
        ctx.headers["Cookie"] = response_ctx.cookie.as_cookie_header_value()
    for k, v in request_ctx.body_params.items():
        value = _find_value_in_new_response(v, prev_response_ctx, response_ctx)
        if value is not None:
            ctx.body_params[k] = value

    return ctx


def sequential_requests(entries, update_dynamic_elements=False, **kwargs):
    req_res = []
    prev_response_context = None
    response = None
    for entry in entries:
        context = entry.request.as_http_request_context()
        if update_dynamic_elements:
            context = _update_dynamic_elements(
                prev_response_ctx=prev_response_context,
                response_ctx=response,
                request_ctx=context
            )
        for k, v in kwargs.items():
            setattr(context, k, v)
        response = http.request_from_context(context=context)
        prev_response_context = entry.response.as_http_response()

        req_res.append((context, response))

    return req_res
