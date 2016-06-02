from sdklib.http import HttpSdk


class SampleHttpsHttpSdk(HttpSdk):

    DEFAULT_HOST = "https://www.carniceriasdejuan.com"

    API_PRODUCTS_PATH = "/api/1.0/products/"

    def get_products(self):
        """
        Get all products.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_PRODUCTS_PATH)
