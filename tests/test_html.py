# -*- coding: utf-8 -*-

import unittest

from sdklib.html.base import HTML


class TestHTML(unittest.TestCase):

    def setUp(self):
        with open("tests/resources/test.html", "r") as f:
            self.html = HTML(f.read())

    def test_find_element_by_id(self):
        self.assertEqual("nav-main mega-menu menu_float_left", self.html.find_element_by_id('primary-nav').get("class"))

    def test_find_by_elements_id(self):
        self.assertEqual(2, len(self.html.find_elements_by_id('primary-nav')))

    def test_find_element_by_xpath(self):
        item = self.html.find_element_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual("Press Room", item.text)

    def test_find_elements_by_xpath(self):
        items = self.html.find_elements_by_xpath("//li[@class='dropdown-submenu test']/a[@href='index.html#']")
        self.assertEqual(1, len(items))
