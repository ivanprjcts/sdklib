from lxml import etree

from sdklib.compat import StringIO


class HTML(object):
    """
    HTMLObject class.

    .. note::

       This class emulates some methods of selenium Web Driver.
       See `selenium Web Driver <https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webdriver.py>`_.
    """

    def __init__(self, dom):
        self._parse(dom=dom)

    def _parse(self, dom):
        parser = etree.HTMLParser()
        self.tree = etree.parse(StringIO(dom), parser)

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
        e = self.tree.xpath(xpath)
        if isinstance(e, list):
            return e[0]
        return e

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:
        """
        return self.tree.xpath(xpath)
