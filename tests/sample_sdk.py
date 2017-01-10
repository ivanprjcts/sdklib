from sdklib.http import HttpSdk
from sdklib.util.parser import parse_args, safe_add_end_slash


class SampleHttpSdk(HttpSdk):
    """
    Sample Sdk for testing purposes.
    """

    DEFAULT_HOST = "https://mockapi.sdklib.org"

    API_ITEMS_URL_PATH = "/items/"

    def get_items(self):
        """
        Get all items.
        :return: SdkResponse
        """
        return self._http_request("GET", self.API_ITEMS_URL_PATH)

    def create_item(self, name, description=None, city=None):
        """
        Create an item.
        :return: SdkResponse
        """
        params = parse_args(name=name, description=description)
        return self._http_request("POST", self.API_ITEMS_URL_PATH, body_params=params)

    def update_item(self, item_id, name, description=None):
        """
        Update an item.
        :return: SdkResponse
        """
        params = parse_args(name=name, description=description)
        return self._http_request("PUT", self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id), body_params=params)
