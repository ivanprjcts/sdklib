import re


def urlsplit(url):
    p = '((?P<scheme>https?)?.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

    m = re.search(p, url)
    scheme = m.group('scheme')
    host = m.group('host')
    port = m.group('port')

    return scheme, host, port
