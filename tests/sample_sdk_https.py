from sdklib.http import HttpSdk


class SampleHttpsHttpSdk(HttpSdk):

    DEFAULT_HOST = "https://www.carniceriasdejuan.com"

    API_PRODUCTS_PATH = "/api/1.0/products/"
    API_CHECKOUT_PATH = "/checkout"

    def get_products(self):
        """
        Get all products.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_PRODUCTS_PATH)

    def checkout(self, redirect=True):
        return self._http_request("GET", self.API_CHECKOUT_PATH, redirect=redirect)
