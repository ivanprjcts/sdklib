from sdklib.html.base import HTML5libMixin, HTMLLxmlMixin, AbstractBaseHTMLElem


class ElemLxml(HTMLLxmlMixin, AbstractBaseHTMLElem):
    """
    Elem class using lxml.
    """

    def __init__(self, lxml_elem):
        self.html_obj = lxml_elem


class Elem5lib(HTML5libMixin, AbstractBaseHTMLElem):
    """
    Elem class using html5lib.
    """
    def __init__(self, html5lib_obj):
        self.html_obj = html5lib_obj
