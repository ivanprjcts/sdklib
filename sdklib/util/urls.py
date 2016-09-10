import re


def urlsplit(url):
    p = '((?P<scheme>.*)?.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

    m = re.search(p, url)
    scheme = m.group('scheme')
    host = m.group('host')
    port = m.group('port')

    return scheme, host, port


def get_hostname_parameters_from_url(url):
    scheme, host, port = urlsplit(url)
    scheme = scheme or 'http'
    host = host or '127.0.0.1'
    port = port or ('443' if scheme == 'https' else '80')
    return scheme, host, port


def ensure_url_path_starts_with_slash(url_path):
    if not url_path:
        return '/'
    if not url_path.startswith('/'):
        return '/' + url_path
    return url_path


def ensure_url_path_format_suffix_starts_with_dot(format_suffix):
    if not format_suffix:
        return ''
    if not format_suffix.startswith('.'):
        return '.' + format_suffix
    return format_suffix
