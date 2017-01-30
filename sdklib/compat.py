import sys


_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    import Cookie as cookies
    from urllib import urlencode, quote_plus
    from urlparse import urlsplit
    import SocketServer as socketserver
    import thread
    from StringIO import StringIO

    basestring = basestring
    bytes = str
    str = unicode
    convert_bytes_to_str = lambda x: x
    convert_unicode_to_native_str = lambda x: x.encode("ISO-8859-1") if isinstance(x, unicode) else x
    convert_str_to_bytes = lambda x: x.encode("ISO-8859-1") if isinstance(x, basestring) else x

elif is_py3:
    from urllib.parse import urlencode, quote_plus, urlsplit
    from urllib.parse import urlencode
    from http import cookies
    import socketserver
    import _thread as thread
    from io import StringIO

    basestring = (str, bytes)
    str = str
    bytes = bytes
    convert_bytes_to_str = lambda x: x.decode() if isinstance(x, bytes) else x
    convert_unicode_to_native_str = lambda x: x
    convert_str_to_bytes = lambda x: x.encode("ISO-8859-1") if isinstance(x, str) else x

try:
    import lxml
    html_lxml = True
except:
    html_lxml = False



