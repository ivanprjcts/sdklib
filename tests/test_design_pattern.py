import unittest

from sdklib.util.design_pattern import Singleton


class MyClass(object):

    attribute = "MyClass"

    def return_hello(self, name):
        return self.attribute + " say hello to " + name


@Singleton
class MySingletonClass(MyClass):
    pass


class TestDesignPattern(unittest.TestCase):
    def test_singleton_try_to_use_standard_init_method(self):
        try:
            c = MySingletonClass()
            self.assertTrue(False)
        except TypeError:
            pass

    def test_singleton_get_instance(self):
        c = MySingletonClass.get_instance()
        res = c.return_hello("ivan")
        self.assertEqual("MyClass say hello to ivan", res)

    def test_singleton_instance_check(self):
        c = MySingletonClass.get_instance()
        self.assertTrue(isinstance(c, MyClass))
