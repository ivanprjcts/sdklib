import urllib3
from sdklib.compat import cache  # noqa: F401


def disable_warnings():
    urllib3.disable_warnings()
