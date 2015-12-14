from sdklib import SdkBase, SdkResponse
from sdklib.util.parser import parse_args


class SampleSdk(SdkBase):

    API_HOST = "ajax.googleapis.com"
    API_SCHEME = "http"
    API_PORT = 80

    API_SEARCH_WEB_PATH = "/ajax/services/search/web"

    def _http(self, method, url, headers=None, form_params=None, query_params=None, ssl_verified=False,
              form_urlencoding=True):
        status, content, headers = super(SampleSdk, self)._http(method, url, headers=headers, form_params=form_params,
                                                                query_params=query_params, ssl_verified=ssl_verified,
                                                                form_urlencoding=form_urlencoding)
        return status, SdkResponse(content), headers

    def search(self, query, version=None):
        """
        Search web pages.
        :param query:
        :param version:
        :return: status, data, headers
        """
        query_params = parse_args(q=query, v=version)
        return self._http("GET", self.API_SEARCH_WEB_PATH, query_params=query_params)