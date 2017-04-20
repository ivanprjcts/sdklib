import html5lib

from sdklib.compat import StringIO, str, convert_bytes_to_str
from sdklib.html.base import HTMLLxmlMixin, AbstractBaseHTML, HTML5libMixin


class HTML5lib(HTML5libMixin, AbstractBaseHTML):
    """
    HTML class using html5lib parser.
    """
    def __init__(self, dom):
        self._parse(dom=dom)
        self._remove_namespaces()

    def _parse(self, dom):
        self.html_obj = html5lib.parse(dom)

    def _remove_namespaces(self):
        for el in self.html_obj.iter():
            if isinstance(el.tag, str) and '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]  # strip all namespaces


class HTMLxml(HTMLLxmlMixin, AbstractBaseHTML):
    """
    HTML class using lxml parser.
    """
    def __init__(self, dom):
        self._parse(dom=dom)

    def _parse(self, dom):
        from lxml import etree

        parser = etree.HTMLParser()
        self.html_obj = etree.parse(StringIO(convert_bytes_to_str(dom)), parser)
