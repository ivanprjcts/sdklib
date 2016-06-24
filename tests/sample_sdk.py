from sdklib.http import HttpSdk
from sdklib.http.renderers import MultiPartRenderer, FormRenderer
from sdklib.util.parser import parse_args


class SampleHttpSdk(HttpSdk):
    """
    Sample Sdk for testing purposes.
    """

    API_RESTAURANTS_URL_PATH = "/api/1.0/restaurants/"
    LOGIN_URL_PATH = "/api/1.0/auth/login/"  # overwrite HttpSdk 'LOGIN_URL_PATH'

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
        return self._http_request("POST", self.API_RESTAURANTS_URL_PATH, body_params=params, render=FormRenderer())

    def update_restaurant(self, name, main_image, description=None, city=None):
        """
        Update a restaurant.
        :return: SdkResponse
        """
        params = parse_args(name=name, description=description, city=city)
        files = parse_args(mainImage=main_image)
        return self._http_request("PUT", self.API_RESTAURANTS_URL_PATH, body_params=params, files=files,
                                  render=MultiPartRenderer())
