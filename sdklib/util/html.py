import exceptions

from xml.etree import ElementTree


class By(object):
    """
    Set of supported locator strategies.
    """

    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"


class HTMLObject(object):

    def __init__(self, html_string=None):
        self.root = ElementTree.fromstring(html_string) if html_string is not None else None

    def from_string(self, html_string):
        self.root = ElementTree.fromstring(html_string)

    def find_element_by_id(self, id_):
        """Finds an element by id.
        :Args:
         - id\_ - The id of the element to be found.
        :Usage:
            html.find_element_by_id('foo')
        """
        return self._find_element(by=By.ID, value=id_)

    def find_elements_by_id(self, id_):
        """
        Finds multiple elements by id.
        :Args:
         - id\_ - The id of the elements to be found.
        :Usage:
            html.find_elements_by_id('foo')
        """
        return self._find_elements(by=By.ID, value=id_)

    def find_element_by_name(self, name):
        """
        Finds an element by name.
        :Args:
         - name: The name of the element to find.
        :Usage:
            html.find_element_by_name('foo')
        """
        return self._find_element(by=By.NAME, value=name)

    def find_elements_by_name(self, name):
        """
        Finds elements by name.
        :Args:
         - name: The name of the elements to find.
        :Usage:
            html.find_elements_by_name('foo')
        """
        return self._find_elements(by=By.NAME, value=name)

    def find_element_by_xpath(self, xpath):
        """
        Finds an element by xpath.
        :Args:
         - xpath - The xpath locator of the element to find.
        :Usage:
            html.find_element_by_xpath('//div/td[1]')
        """
        return self._find_element(by=By.XPATH, value=xpath)

    def find_elements_by_xpath(self, xpath):
        """
        Finds multiple elements by xpath.
        :Args:
         - xpath - The xpath locator of the elements to be found.
        :Usage:
            html.find_elements_by_xpath("//div[contains(@class, 'foo')]")
        """
        return self._find_elements(by=By.XPATH, value=xpath)

    @staticmethod
    def _get_xpath(by, value):
        if by == By.ID:
            value = './/*[id="%s"]' % value
        elif by == By.TAG_NAME:
            pass
        elif by == By.CLASS_NAME:
            pass
        elif by == By.NAME:
            value = './/*[name="%s"]' % value
        return value

    def _find_element(self, by=By.ID, value=None):
        """
        'Private' method used by the find_element_by_* methods.
        :Usage:
            Use the corresponding find_element_by_* instead of this.
        :rtype: Element
        """
        if self.root is None:
            raise exceptions.BaseException("HTML content not found")
        value = self._get_xpath(by=by, value=value)
        return self.root.find(value)

    def _find_elements(self, by=By.ID, value=None):
        """
        'Private' method used by the find_elements_by_* methods.
        :Usage:
            Use the corresponding find_elements_by_* instead of this.
        :rtype: list of Element
        """
        if self.root is None:
            raise exceptions.BaseException("HTML content not found")
        value = self._get_xpath(by=by, value=value)
        return self.root.findall(value)
