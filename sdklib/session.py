# -*- coding: utf-8 -*-

from .compat import cookies


class Cookie(object):

    def __init__(self, headers=None):
        self._cookie = None
        self.load_from_set_cookie_header(headers)

    def load_from_set_cookie_header(self, headers):
        if not headers:
            return
        set_cookie_header = headers.get("Set-Cookie")
        if set_cookie_header:
            ck = cookies.SimpleCookie()
            ck.load(set_cookie_header)
            self._cookie = ck

    def output_cookie_header_value(self):
        if not self._cookie:
            return ""
        items = self._cookie.items()
        if len(items) == 0:
            return ""
        name, morsel = items[0]
        output = "%s=%s" % (name, morsel.value)
        for name, morsel in items[1:]:
            output += "; "
            output += "%s=%s" % (name, morsel.value)
        return output

    def getcookie(self):
        return self._cookie

    def get(self, key, default=None):
        return self._cookie.get(key , default)


