import unittest

from sdklib.util.design_pattern import Singleton


@Singleton
class MyClass:

    attribute = "MyClass"

    def return_hello(self, name):
        return self.attribute + " say hello to " + name


class TestDesignPattern(unittest.TestCase):

    def test_singleton_try_to_use_standard_init_method(self):
        try:
            c = MyClass()
            self.assertTrue(False)
        except TypeError:
            pass

    def test_singleton_get_instance(self):
        c = MyClass.get_instance()
        res = c.return_hello("ivan")
        self.assertEqual("MyClass say hello to ivan", res)
