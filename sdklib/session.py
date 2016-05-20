# -*- coding: utf-8 -*-

from .compat import cookies


def load_set_cookie_header(headers):
    set_cookie_header = headers.get("Set-Cookie")
    c = cookies.SimpleCookie()
    if set_cookie_header:
        c.load(set_cookie_header)
    return c


def output_cookie_header_value(cookie):
    return cookie.output(header="Cookie:")