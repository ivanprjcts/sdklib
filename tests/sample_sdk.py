import time

from sdklib.http import HttpSdk
from sdklib.util.parser import parse_args, safe_add_end_slash
from sdklib.http.authorization import X11PathsAuthentication
from sdklib.shortcuts import cache


class SampleHttpSdk(HttpSdk):
    """
    Sample Sdk for testing purposes.
    """

    DEFAULT_HOST = "https://www.google.es"

    LOGIN_URL_PATH = "/login/"  # not exist
    API_ITEMS_URL_PATH = "/items/"
    API_FILE_URL_PATH = "/files/"

    def get_items(self):
        """
        Get all items.

        :return: SdkResponse
        """
        return self.get(self.API_ITEMS_URL_PATH)

    @cache(maxsize=None)
    def get_items_with_cache(self):
        """
        Get all items.

        :return: SdkResponse
        """
        time.sleep(8)
        return self.get(self.API_ITEMS_URL_PATH)

    def get_items_with_empty_query_params_parameter(self):
        """
        Get all items.

        :return: SdkResponse
        """
        params = {}
        return self.get(self.API_ITEMS_URL_PATH, query_params=params)

    def create_item(self, name, description=None, city=None):
        """
        Create an item.

        :return: SdkResponse
        """
        params = parse_args(name=name, description=description)
        return self.post(self.API_ITEMS_URL_PATH, body_params=params)

    def update_item(self, item_id, name, description=None):
        """
        Update an item.

        :return: SdkResponse
        """
        params = parse_args(name=name, description=description)
        return self.put(self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id), body_params=params)

    def partial_update_item(self, item_id, name=None, description=None):
        """
        Update partially an item.

        :return: SdkResponse
        """
        params = parse_args(name=name, description=description)
        return self.patch(self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id), body_params=params)

    def delete_item(self, item_id):
        """
        Delete an item.

        :return: SdkResponse
        """
        return self.delete(self.API_ITEMS_URL_PATH + safe_add_end_slash(item_id))

    def create_file_11paths_auth(self, filename, file_stream, app_id, secret, description=None, name=None):
        """
        Create a file using 11paths authentication.

        :return: SdkResponse
        """
        auth = (X11PathsAuthentication(app_id, secret),)
        params = parse_args(name=name, description=description)
        return self.post(self.API_FILE_URL_PATH, body_params=params, files={"file": (filename, file_stream)},
                         authentication_instances=auth, host="https://latch.elevenpaths.com")
