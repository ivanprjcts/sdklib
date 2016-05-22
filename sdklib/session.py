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
        output = ""
        if self._cookie:
            output = self._cookie.output(header="", sep=";")
        if len(output) > 0 and output[0] == ' ':
            output = output[1:]
        return output

    def getcookie(self):
        return self._cookie


