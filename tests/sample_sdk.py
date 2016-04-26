from sdklib import SdkBase


class SampleSdk(SdkBase):
    DEFAULT_HOST = "http://demoapp.allergicucaneat.com"

    API_SEARCH_WEB_PATH = "/api/1.0/restaurants/"

    def get_restaurants(self):
        """
        Get all restaurants.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_SEARCH_WEB_PATH)