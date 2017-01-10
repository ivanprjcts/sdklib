from sdklib.http import HttpSdk


class SampleHttpsHttpSdk(HttpSdk):

    DEFAULT_HOST = "https://www.projectx.com.es"

    API_PRODUCTS_PATH = "/api/1.0/products/"
    API_CHECKOUT_PATH = "/checkout"
    API_HOME_PATH = "/"

    def get_products(self):
        """
        Get all products.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_PRODUCTS_PATH)

    def checkout(self, redirect=True):
        return self._http_request("GET", self.API_CHECKOUT_PATH, redirect=redirect)

    def home(self):
        return self._http_request("GET", self.API_HOME_PATH)
