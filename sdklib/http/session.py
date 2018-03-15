# -*- coding: utf-8 -*-

from urllib3._collections import HTTPHeaderDict
from sdklib.compat import cookies


class Cookie(object):
    """
    Wrapper of python Cookie class.

    See https://docs.python.org/2/library/cookie.html
    """

    def __init__(self, headers=None):
        self._cookie = cookies.SimpleCookie()
        self.load_from_headers(headers)

    def load_from_headers(self, headers):
        if not headers:
            return
        elif not isinstance(headers, HTTPHeaderDict):
            headers = HTTPHeaderDict(headers)
        set_cookie_headers = headers.getlist("Set-Cookie")
        if set_cookie_headers:
            self._cookie.load("; ".join(set_cookie_headers))

    def as_cookie_header_value(self):
        if self.is_empty():
            return ""
        items = list(self.items())
        name, morsel = items[0]
        output = "%s=%s" % (name, morsel.value)
        for name, morsel in items[1:]:
            output += "; "
            output += "%s=%s" % (name, morsel.value)
        return output

    def is_empty(self):
        return (self._cookie is None) or (len(self._cookie.items()) == 0)

    def getcookie(self):
        return self._cookie

    def items(self):
        return self._cookie.items()

    def get(self, key, default=None):
        return self._cookie.get(key, default)

    def update(self, cookie):
        for key, morsel in cookie.items():
            self._cookie[key] = morsel.value
