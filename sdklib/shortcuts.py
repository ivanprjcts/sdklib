import urllib3
from sdklib.compat import cache


def disable_warnings():
    urllib3.disable_warnings()
