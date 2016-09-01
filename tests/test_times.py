import unittest
import time

from sdklib.util.times import timeout


class TestTimes(unittest.TestCase):

    def test_timeout_under_limit(self):
        @timeout(milliseconds=5000)
        def my_short_function():
            time.sleep(1)
            return "Ok"

        res = my_short_function()
        self.assertEqual(res, "Ok")

    def test_timeout_over_limit_silent(self):
        @timeout(milliseconds=5000, silent=True)
        def my_long_function():
            time.sleep(7)
            return "Ok"

        res = my_long_function()
        self.assertIsNone(res)
