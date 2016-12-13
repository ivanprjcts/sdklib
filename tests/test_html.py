# -*- coding: utf-8 -*-

import unittest

from sdklib.html.base import HTML


class TestHTML(unittest.TestCase):

    def setUp(self):
        with open("tests/resources/test.html", "r") as f:
            self.html = HTML(f.read())

    def test_basic_html(self):
        print self.html

    def test_find_by_id(self):
        print self.html

    def test_find_by_xpath(self):
        for item in self.html.tree.findall(".//{http://www.w3.org/1999/xhtml}a"):
            print item.text
