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


class Urllib3ResponseMock(object):
    def __init__(self):
        self.data = XML_CATALOG


class TestResponse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.response = HttpResponse(Urllib3ResponseMock())

    @classmethod
    def tearDownClass(cls):
        pass

    def test_xml_response_data(self):
        data = self.response.data
        self.assertTrue(isinstance(data["CATALOG"]["CD"], list))

    def test_xml_response(self):
        xml_data = self.response.xml
        self.assertEqual("CATALOG", xml_data.tag)

    def test_xml_response_raw(self):
        xml_raw = self.response.raw
        self.assertIn("<?xml version=\"1.0\"", xml_raw)
