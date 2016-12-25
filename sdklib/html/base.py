import html5lib

from sdklib.compat import StringIO, str, convert_bytes_to_str


class HTMLBase(object):
    """
    HTMLObject abstract class.

    .. note::

       This class emulates some methods of selenium Web Driver.
       See `selenium Web Driver <https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webdriver.py>`_.
    """
    def find_element_by_id(self, id_):
        """
        Finds an element by id.

        :param id_: The id of the element to be found.
        :return:
        """
        return self.find_element_by_xpath('//*[@id="%s"]' % id_)

    def find_elements_by_id(self, id_):
        """
        Finds multiple elements by id.

        :param id_: The id of the elements to be found.
        :return:
        """
        return self.find_elements_by_xpath('//*[@id="%s"]' % id_)

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:
        """
        pass

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:
        """
        pass


class HTMLxml(HTMLBase):
    """
    HTMLObject class using lxml parser.
    """
    def __init__(self, dom):
        self._parse(dom=dom)

    def _parse(self, dom):
        from lxml import etree

        parser = etree.HTMLParser()
        self.tree = etree.parse(StringIO(convert_bytes_to_str(dom)), parser)

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:

        http://lxml.de/xpathxslt.html#xpath
        """
        e = self.tree.xpath(xpath)
        if isinstance(e, list) and len(e) > 0:
            return e[0]

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:

        http://lxml.de/xpathxslt.html#xpath
        """
        return self.tree.xpath(xpath)


class HTML5lib(HTMLBase):
    """
    HTMLObject class using html5lib parser.
    """
    def __init__(self, dom):
        self._parse(dom=dom)
        self._remove_namespaces()

    def _parse(self, dom):
        self.tree = html5lib.parse(dom)

    def _remove_namespaces(self):
        for el in self.tree.iter():
            if isinstance(el.tag, str) and '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces

    @staticmethod
    def _convert_xpath(xpath):
        return "." + xpath if xpath.startswith("/") else xpath

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:

        https://docs.python.org/2/library/xml.etree.elementtree.html#supported-xpath-syntax
        """
        return self.tree.find(self._convert_xpath(xpath))

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:

        https://docs.python.org/2/library/xml.etree.elementtree.html#supported-xpath-syntax
        """
        return self.tree.findall(self._convert_xpath(xpath))
