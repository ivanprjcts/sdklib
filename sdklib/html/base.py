

class AbstractBaseHTML(object):
    """
    HTML base abstract class.

    .. note::

       This class emulates some methods of selenium Web Driver.
       See `selenium Web Driver <https://github.com/SeleniumHQ/selenium/blob/master/py/selenium/webdriver/remote/webdriver.py>`_.
    """
    html_obj = None  # encapsulated html object

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

    def find_element_by_name(self, name):
        """
        Finds an element by name.

        :param name: The name of the element to be found.
        :return:
        """
        return self.find_element_by_xpath('//*[@name="%s"]' % name)

    def find_elements_by_name(self, name):
        """
        Finds multiple elements by name.

        :param name: The name of the elements to be found.
        :return:
        """
        return self.find_elements_by_xpath('//*[@name="%s"]' % name)

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:
        """
        raise NotImplementedError

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:
        """
        raise NotImplementedError


class AbstractBaseHTMLElem(AbstractBaseHTML):
    """
    HTML elem base abstract class.
    """
    @property
    def text(self):
        return self.html_obj.text

    def get(self, attribute):
        return self.html_obj.get(attribute)

    def get_attribute(self, value):
        for k, v in self.html_obj.items():
            if v == value:
                return k


class HTMLLxmlMixin(object):

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return: ElemLxml
        
        See lxml xpath expressions `here <http://lxml.de/xpathxslt.html#xpath>`_
        """
        elems = self.find_elements_by_xpath(xpath)
        if isinstance(elems, list) and len(elems) > 0:
            return elems[0]

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return: list of ElemLxml
        
        See lxml xpath expressions `here <http://lxml.de/xpathxslt.html#xpath>`_
        """
        from sdklib.html.elem import ElemLxml

        elements = self.html_obj.xpath(xpath)
        return [ElemLxml(e) for e in elements]


class HTML5libMixin(object):
    @staticmethod
    def _convert_xpath(xpath):
        return "." + xpath if xpath.startswith("/") else xpath

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.

        :param xpath: The xpath locator of the element to find.
        :return:

        See html5lib xpath expressions `here <https://docs.python.org/2/library/xml.etree.elementtree.html#supported-xpath-syntax>`_
        """
        from sdklib.html.elem import Elem5lib

        return Elem5lib(self.html_obj.find(self._convert_xpath(xpath)))

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.

        :param xpath: The xpath locator of the elements to be found.
        :return:

        See html5lib xpath expressions `here <https://docs.python.org/2/library/xml.etree.elementtree.html#supported-xpath-syntax>`_
        """
        from sdklib.html.elem import Elem5lib

        return [Elem5lib(e) for e in self.html_obj.findall(self._convert_xpath(xpath))]
