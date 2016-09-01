import sys


_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

if is_py2:
    import Cookie as cookies
    from urllib import urlencode, quote_plus
    import SocketServer as socketserver
    import thread

    basestring = basestring
    str = unicode
elif is_py3:
    from urllib.parse import urlencode, quote_plus
    from http import cookies
    import socketserver
    import _thread as thread

    basestring = (str, bytes)
    str = str
