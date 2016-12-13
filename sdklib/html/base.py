import html5lib


class HTML(object):

    def __init__(self, dom):
        self._parse(dom=dom)

    def _parse(self, dom):
        self.tree = html5lib.parse(dom)

    def find_element_by_id(self, id_):
        pass

    def find_element_by_xpath(self, xpath):
        self.tree.findall(xpath)
        return self.tree.findall(xpath)
