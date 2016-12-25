# -*- coding: utf-8 -*-

import unittest

try:
    from exceptions import SyntaxError
except:
    pass


class TestHTML(unittest.TestCase):

    def setUp(self):
        from sdklib.html import HTML

        with open("tests/resources/test.html", "r") as f:
            self.html = HTML(f.read())

    def test_find_element_by_id(self):
        self.assertEqual("nav-main mega-menu menu_float_left", self.html.find_element_by_id('primary-nav').get("class"))

    def test_find_element_by_id_html5lib(self):
        from sdklib.html.base import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        self.assertEqual("nav-main mega-menu menu_float_left", html.find_element_by_id('primary-nav').get("class"))

    def test_find_by_elements_id(self):
        self.assertEqual(2, len(self.html.find_elements_by_id('primary-nav')))

    def test_find_by_elements_id_html5lib(self):
        from sdklib.html.base import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        self.assertEqual(2, len(html.find_elements_by_id('primary-nav')))

    def test_find_element_by_xpath(self):
        item = self.html.find_element_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual("Press Room", item.text)

    def test_find_element_by_xpath_html5lib(self):
        from sdklib.html.base import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        item = html.find_element_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual("Press Room", item.text)

    def test_find_elements_by_xpath(self):
        items = self.html.find_elements_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual(1, len(items))

    def test_find_elements_by_xpath_html5lib(self):
        from sdklib.html.base import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        items = html.find_elements_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual(1, len(items))

    def test_find_element_by_xpath_contains(self):
        item = self.html.find_element_by_xpath("//li[contains(@class, 'test')]/a[@href='index.html#']")
        self.assertEqual("Press Room", item.text)

    def test_find_element_by_xpath_contains_html5lib(self):
        from sdklib.html.base import HTML5lib
        with open("tests/resources/test.html", "r") as f:
            html = HTML5lib(f.read())

        try:
            html.find_element_by_xpath("//li[contains(@class, 'test')]/a[@href='index.html#']")
            self.assertTrue(False)
        except SyntaxError:
            pass
