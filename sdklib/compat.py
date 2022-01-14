import sys


_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    import Cookie as cookies
    from urllib import urlencode, quote_plus, unquote_plus
    from urlparse import urlsplit
    import SocketServer as socketserver
    import thread
    from StringIO import StringIO
    import exceptions

    py_bytes = bytes
    basestring = basestring  # noqa: F821
    bytes = str
    str = unicode  # noqa: F821
    convert_bytes_to_str = lambda x: x  # noqa: E731
    convert_unicode_to_native_str = lambda x: x.encode("ISO-8859-1") \
        if isinstance(x, unicode) else x  # noqa: E731,F821
    convert_str_to_bytes = lambda x: py_bytes(x)  # noqa: E731

    def cache(*args, **kargs):
        def wrapper(f):
            def real_wrapper(*args, **kwargs):
                raise exceptions.NotImplementedError("Only available for python 3.2. or +.")
            return real_wrapper
        return wrapper


elif is_py3:
    from urllib.parse import urlencode, quote_plus, urlsplit, unquote_plus  # noqa: F401
    from http import cookies  # noqa: F401
    import socketserver  # noqa: F401
    import _thread as thread  # noqa: F401
    from io import StringIO  # noqa: F401
    from functools import lru_cache as cache  # noqa: F401
    from sdklib import _exceptions as exceptions

    basestring = (str, bytes)
    str = str
    bytes = bytes
    convert_bytes_to_str = lambda x: x.decode() if isinstance(x, bytes) else x  # noqa: E731
    convert_unicode_to_native_str = lambda x: x  # noqa: E731
    convert_str_to_bytes = lambda x: x.encode("ISO-8859-1") \
        if isinstance(x, str) else x  # noqa: E731

try:
    import lxml  # noqa: F401
    html_lxml = True
except Exception:
    html_lxml = False
