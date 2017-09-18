# -*- coding: utf-8 -*-

import unittest

try:
    from exceptions import SyntaxError
except:
    pass


class TestHTMLElem(unittest.TestCase):

    def setUp(self):
        from sdklib.html import HTML

        with open("tests/resources/test.html", "r") as f:
            self.html = HTML(f.read())

    def test_find_element_by_id_and_find_element_by_xpath(self):
        elem = self.html.find_element_by_id('primary-nav')
        self.assertEqual("Our company", elem.find_element_by_xpath("//*[@href='company/index.html']").text)

    def test_find_elements_by_id_and_find_element_by_xpath(self):
        elems = self.html.find_elements_by_id('primary-nav')
        self.assertEqual(2, len(elems))
        self.assertEqual("Our company", elems[0].find_element_by_xpath("//*[@href='company/index.html']").text)

    def test_find_element_by_id_and_find_element_by_xpath_html5lib(self):
        from sdklib.html.html import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        elem = html.find_element_by_id('primary-nav')
        self.assertEqual("Our company", elem.find_element_by_xpath("//*[@href='company/index.html']").text)

    def test_find_elements_by_id_and_find_element_by_xpath_html5lib(self):
        from sdklib.html.html import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        elems = html.find_elements_by_id('primary-nav')
        self.assertEqual(2, len(elems))
        self.assertEqual("Our company", elems[0].find_element_by_xpath("//*[@href='company/index.html']").text)

    def test_get_attribute(self):
        elem = self.html.find_element_by_id('primary-nav')
        self.assertEqual("class", elem.get_attribute("nav-main mega-menu menu_float_left"))

    def test_get_attribute_html5lib(self):
        from sdklib.html.html import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        elem = html.find_element_by_id('primary-nav')
        self.assertEqual("class", elem.get_attribute("nav-main mega-menu menu_float_left"))

    def test_get_parent(self):
        elem = self.html.find_element_by_id('child-elem')
        self.assertEqual("hello", elem.getparent().get("class"))

    def test_get_parent_with_height(self):
        elem = self.html.find_element_by_id('child-elem')
        self.assertEqual("events-menu mega-menu-item mega-menu-fullwidth dropdown-submenu",
                         elem.getparent(height=3).get("class"))

    def test_get_non_existing_parent(self):
        elem = self.html.find_element_by_id('child-elem')
        self.assertIsNone(elem.getparent(height=20))
