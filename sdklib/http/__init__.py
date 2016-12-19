from sdklib.http.sdk_base import HttpSdk, HttpRequestContext, generate_url_path
from sdklib.http.response import HttpResponse
from sdklib.http.renderers import get_renderer, url_encode
from sdklib.util.design_pattern import Singleton


__all__ = [
    'HttpSdk', 'HttpResponse', 'get_renderer', 'HttpRequestContext', 'api', 'HttpRequestContextSingleton', 'url_encode',
    'generate_url_path'
]


api = HttpSdk()


@Singleton
class HttpRequestContextSingleton(HttpRequestContext):
    pass
