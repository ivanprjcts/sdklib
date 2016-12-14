import unittest

from sdklib.http import HttpResponse


XML_CATALOG = """<?xml version="1.0" encoding="UTF-8"?>
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

HTML_STR = """<!DOCTYPE html>
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


class Urllib3ResponseMock(object):
    def __init__(self, data):
        self.data = data


class TestResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xml_response = HttpResponse(Urllib3ResponseMock(XML_CATALOG))
        cls.html_response = HttpResponse(Urllib3ResponseMock(HTML_STR))

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
        self.assertIn("<?xml version=\"1.0\"", xml_raw)

    def test_html_response(self):
        html = self.html_response.html
        self.assertIn("This is a Heading", html.find_element_by_id("heading").text)
