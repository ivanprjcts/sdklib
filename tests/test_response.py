import unittest

from sdklib.http.response import Api11PathsResponse, HttpResponse


XML_CATALOG = b"""<?xml version="1.0" encoding="UTF-8"?>
<CATALOG>
    <CD>
        <TITLE>Empire Burlesque</TITLE>
        <ARTIST>Bob Dylan</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>Columbia</COMPANY>
        <PRICE>10.90</PRICE>
        <YEAR>1985</YEAR>
    </CD>
    <CD>
        <TITLE>Hide your heart</TITLE>
        <ARTIST>Bonnie Tyler</ARTIST>
        <COUNTRY>UK</COUNTRY>
        <COMPANY>CBS Records</COMPANY>
        <PRICE>9.90</PRICE>
        <YEAR>1988</YEAR>
    </CD>
    <CD>
        <TITLE>Greatest Hits</TITLE>
        <ARTIST>Dolly Parton</ARTIST>
        <COUNTRY>USA</COUNTRY>
        <COMPANY>RCA</COMPANY>
        <PRICE>9.90</PRICE>
        <YEAR>1982</YEAR>
    </CD>
</CATALOG>
"""

HTML_STR = b"""<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1 id="heading">This is a Heading</h1>
<p>This is a paragraph.</p>

</body>
</html>
"""

JSON_DATA_AND_ERROR = b"""{"data": "Hello","error":{"code":209,"message":"No available cleanings"}}"""
INSENSITIVE_JSON_DATA_AND_ERROR = b"""{"DaTA": "Hello","eRror":{"codE":209,"Message":"No available cleanings"}}"""
JSON_NULL_DATA_AND_ERROR = b"""{"data":null,"error":null}"""
JSON_NO_DATA_AND_ERROR = b"""{}"""
JSON_ERROR_CODE_AND_NO_MESSAGE = b"""{"error":{"code":209}}"""


class Urllib3ResponseMock(object):
    def __init__(self, data):
        self.data = data

    def getheaders(self):
        return {}

    @property
    def status(self):
        return None

    @property
    def reason(self):
        return None


class TestResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xml_response = HttpResponse(Urllib3ResponseMock(XML_CATALOG))
        cls.html_response = HttpResponse(Urllib3ResponseMock(HTML_STR))
        cls.api11paths_response_null_data = Api11PathsResponse(Urllib3ResponseMock(JSON_NULL_DATA_AND_ERROR))
        cls.api11paths_response_data_error = Api11PathsResponse(Urllib3ResponseMock(JSON_DATA_AND_ERROR))
        cls.api11paths_response_no_data = Api11PathsResponse(Urllib3ResponseMock(JSON_NO_DATA_AND_ERROR))
        cls.api11paths_response_error_code_no_message = Api11PathsResponse(
            Urllib3ResponseMock(JSON_ERROR_CODE_AND_NO_MESSAGE)
        )
        cls.api11paths_response_insensitive_data_error = Api11PathsResponse(
            Urllib3ResponseMock(INSENSITIVE_JSON_DATA_AND_ERROR)
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_xml_response_data(self):
        data = self.xml_response.data
        self.assertTrue(isinstance(data["CATALOG"]["CD"], list))

    def test_xml_response(self):
        xml_data = self.xml_response.xml
        self.assertEqual("CATALOG", xml_data.tag)

    def test_xml_response_raw(self):
        xml_raw = self.xml_response.raw
        self.assertEqual(XML_CATALOG, xml_raw)

    def test_html_response(self):
        html = self.html_response.html
        self.assertIn("This is a Heading", html.find_element_by_id("heading").text)

    def test_api11paths_response_data_and_error(self):
        data = self.api11paths_response_data_error.data
        error = self.api11paths_response_data_error.error
        self.assertEqual("Hello", data)
        self.assertEqual("No available cleanings", error.message)
        self.assertEqual(209, error.code)

    def test_api11paths_response_null_data_error(self):
        data = self.api11paths_response_null_data.data
        error = self.api11paths_response_null_data.error
        self.assertIsNone(data)
        self.assertIsNone(error)

    def test_api11paths_response_error_code_no_message(self):
        data = self.api11paths_response_error_code_no_message.data
        error = self.api11paths_response_error_code_no_message.error
        self.assertIsNone(data)
        self.assertEqual(209, error.code)
        self.assertEqual(None, error.message)

    def test_api11paths_response_no_data_error(self):
        data = self.api11paths_response_null_data.data
        error = self.api11paths_response_null_data.error
        self.assertIsNone(data)
        self.assertIsNone(error)

    def test_api11paths_response_insensitive_data_and_error(self):
        data = self.api11paths_response_insensitive_data_error.data
        error = self.api11paths_response_insensitive_data_error.error
        self.assertEqual("Hello", data)
        self.assertEqual("No available cleanings", error.message)
        self.assertEqual(209, error.code)
