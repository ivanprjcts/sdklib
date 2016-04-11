from sdklib import SdkBase, SdkResponse


class SampleHttpsSdk(SdkBase):

    API_HOST = "www.carniceriasdejuan.com"
    API_SCHEME = "https"
    API_PORT = 443

    API_PRODUCTS_PATH = "/api/1.0/products/"

    def _http(self, method, url, headers=None, form_params=None, query_params=None, ssl_verified=False,
              form_urlencoding=True):
        status, content, headers = super(SampleHttpsSdk, self)._http(method, url, headers=headers, form_params=form_params,
                                                                query_params=query_params, ssl_verified=ssl_verified,
                                                                form_urlencoding=form_urlencoding)
        return status, SdkResponse(content), headers

    def get_products(self):
        """
        Get all products.
        :return: status, data, headers
        """
        return self._http("GET", self.API_PRODUCTS_PATH)