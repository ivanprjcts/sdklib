from sdklib import SdkBase, SdkResponse
from sdklib.util.parser import parse_args


class SampleSdk(SdkBase):

    API_HOST = "demoapp.allergicucaneat.com"
    API_SCHEME = "http"
    API_PORT = 80

    API_SEARCH_WEB_PATH = "/api/1.0/restaurants/"

    def _http(self, method, url, headers=None, form_params=None, query_params=None, ssl_verified=False,
              form_urlencoding=True):
        status, content, headers = super(SampleSdk, self)._http(method, url, headers=headers, form_params=form_params,
                                                                query_params=query_params, ssl_verified=ssl_verified,
                                                                form_urlencoding=form_urlencoding)
        return status, SdkResponse(content), headers

    def get_restaurants(self):
        """
        Get all restaurants.
        :return: status, data, headers
        """
        return self._http("GET", self.API_SEARCH_WEB_PATH)