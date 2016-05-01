from sdklib import SdkBase
from sdklib.util.parser import parse_args
from sdklib.renderers import JSONRender, PlainTextRender, MultiPartRender, FormRender


class SampleSdk(SdkBase):
    DEFAULT_HOST = "http://demoapp.allergicucaneat.com"

    API_RESTAURANTS_URL_PATH = "/api/1.0/restaurants/"
    LOGIN_URL_PATH = "/api/1.0/auth/login/"  # overwrite SdkBase 'LOGIN_URL_PATH'

    def get_restaurants(self):
        """
        Get all restaurants.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_RESTAURANTS_URL_PATH)

    def create_restaurant(self, name, description=None, city=None):
        """
        Create a restaurant.
        :return: SdkResponse
        """
        params = parse_args(name=name, description=description, city=city)
        return self._http_request("POST", self.API_RESTAURANTS_URL_PATH, body_params=params, render=FormRender())
