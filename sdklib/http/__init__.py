from sdklib.http.sdk_base import HttpSdk, HttpRequestContext
from sdklib.http.response import HttpResponse
from sdklib.http.renderers import get_renderer, url_encode
from sdklib.util.design_pattern import Singleton


__all__ = [
    'HttpSdk', 'HttpResponse', 'get_renderer', 'HttpRequestContext', 'api', 'HttpRequestContextSingleton', 'url_encode'
]


api = HttpSdk()


@Singleton
class HttpRequestContextSingleton(HttpRequestContext):

    def clear(self):
        self.host = None
        self.proxy = None
        self.method = None
        self.url_path = None
        self.headers = None
        self.authentication_instances = []
        self.body_params = None
        self.query_params = None
        self.files = None
        self.renderer = None
