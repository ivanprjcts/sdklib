# -*- coding: utf-8 -*-

from sdklib.compat import cookies


class Cookie(object):
    """
    Wrapper of python Cookie class.

    See https://docs.python.org/2/library/cookie.html
    """

    def __init__(self, headers=None):
        self._cookie = None
        self.load_from_headers(headers)

    def load_from_headers(self, headers):
        if not headers:
            return
        set_cookie_header = headers.get("Set-Cookie")
        if set_cookie_header:
            ck = cookies.SimpleCookie()
            ck.load(set_cookie_header)
            self._cookie = ck

    def as_cookie_header_value(self):
        if self.is_empty():
            return ""
        items = self.items()
        name, morsel = items[0]
        output = "%s=%s" % (name, morsel.value)
        for name, morsel in items[1:]:
            output += "; "
            output += "%s=%s" % (name, morsel.value)
        return output

    def is_empty(self):
        return (self._cookie is None) or (self._cookie.items() == [])

    def getcookie(self):
        return self._cookie

    def items(self):
        return self._cookie.items()

    def get(self, key, default=None):
        return self._cookie.get(key, default)
