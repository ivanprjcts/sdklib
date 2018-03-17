from sdklib.html.base import HTML5libMixin, HTMLLxmlMixin, AbstractBaseHTMLElem


class ElemLxml(HTMLLxmlMixin, AbstractBaseHTMLElem):
    """
    Elem class using lxml.
    """

    def __init__(self, lxml_elem):
        self.html_obj = lxml_elem

    @property
    def text(self):
        text_as_list = []

        node_text = self.html_obj.text.strip() if self.html_obj.text else None
        text_children = [child.tail.strip() for child in self.html_obj.getchildren() if child.tail and child.tail.strip()]

        if node_text: text_as_list.append(node_text.strip())
        text_as_list.extend(text_children)

        return " ".join(text_as_list)

    def getparent(self, height=1):
        parent = self.html_obj
        for _ in range(0, height):
            if parent is not None:
                parent = parent.getparent()
        if parent is not None:
            return ElemLxml(parent)


class Elem5lib(HTML5libMixin, AbstractBaseHTMLElem):
    """
    Elem class using html5lib.
    """
    def __init__(self, html5lib_obj):
        self.html_obj = html5lib_obj
