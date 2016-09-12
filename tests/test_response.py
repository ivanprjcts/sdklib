import unittest

from sdklib.http import HttpSdk


class SampleHttpSdk(HttpSdk):
    """
    Sample XML Sdk for testing purposes.
    """
    DEFAULT_HOST = "http://www.w3schools.com"

    XML_CATALOG_URL_PATH = "/xml/cd_catalog.xml"

    def get_catalog(self):
        """
        Get XML Catalog.
        :return: SdkResponse
        """
        return self._http_request("GET", self.XML_CATALOG_URL_PATH)


class TestResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        api = SampleHttpSdk()
        cls.response = api.get_catalog()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_xml_response_data(self):
        data = self.response.data
        self.assertTrue(isinstance(data["CATALOG"]["CD"], list))

    def test_xml_response(self):
        xml_data = self.response.xml
        self.assertEqual("CATALOG", xml_data.tag)
