import urllib3


__version__ = '1.9.3'


def disable_warnings():
    urllib3.disable_warnings()
