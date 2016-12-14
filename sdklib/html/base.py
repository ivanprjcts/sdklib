import html5lib

from sdklib.compat import str


class HTML(object):
    """
    HTMLObject class.

    .. note::

       This class emulates some methods of selenium Web Driver.
       See `selenium Web Driver <https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webdriver.py>`_.
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

    def find_element_by_id(self, id_):
        """
        Finds an element by id.

        :param id_: The id of the element to be found.
        :return:
        """
        return self.find_element_by_xpath('.//*[@id="%s"]' % id_)

    def find_elements_by_id(self, id_):
        """
        Finds multiple elements by id.

        :param id_: The id of the elements to be found.
        :return:
        """
        return self.find_elements_by_xpath('.//*[@id="%s"]' % id_)

    @staticmethod
    def _convert_xpath(xpath):
        return "." + xpath if xpath.startswith("/") else xpath

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:
        """
        return self.tree.find(self._convert_xpath(xpath))

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:
        """
        return self.tree.findall(self._convert_xpath(xpath))
