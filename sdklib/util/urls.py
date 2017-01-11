import re

from sdklib.compat import urlencode, str, urlsplit as py_urlsplit


def urlsplit(url):
    """
    Split url into scheme, host, port, path, query

    :param str url:
    :return: scheme, host, port, path, query
    """
    p = '((?P<scheme>.*)?.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
    m = re.search(p, url)
    scheme = m.group('scheme')
    host = m.group('host')
    port = m.group('port')

    _scheme, _netloc, path, query, _fragment = tuple(py_urlsplit(url))

    return scheme, host, port, path, query


def _get_scheme_or_default(scheme):
    return scheme or 'http'


def _get_host_or_default(host):
    return host or '127.0.0.1'


def _get_port_or_default(port, scheme):
    return port or ('443' if scheme == 'https' else '80')


def get_hostname_parameters_from_url(url):
    scheme, host, port, _, _ = urlsplit(url)
    scheme = _get_scheme_or_default(scheme)
    host = _get_host_or_default(host)
    port = _get_port_or_default(port, scheme=scheme)
    return scheme, host, port


def _ensure_str_starts_with(_str, beginning, default=''):
    if not _str:
        return default
    if not _str.startswith('/'):
        return beginning + _str
    return _str


def ensure_url_path_starts_with_slash(url_path):
    return _ensure_str_starts_with(url_path, '/', default='/')


def ensure_url_path_format_suffix_starts_with_dot(format_suffix):
    return _ensure_str_starts_with(format_suffix, '.', default='')


def generate_url(scheme=None, host=None, port=None, path=None, query=None):
    """
    Generate URI from parameters.

    :param str scheme:
    :param str host:
    :param int port:
    :param str path:
    :param dict query:
    :return:
    """
    url = ""
    if scheme is not None:
        url += "%s://" % scheme
    if host is not None:
        url += host
    if port is not None:
        url += ":%s" % str(port)
    if path is not None:
        url += ensure_url_path_starts_with_slash(path)
    if query is not None:
        url += "?%s" % (urlencode(query))
    return url
