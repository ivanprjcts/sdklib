import unittest
import time
from datetime import timedelta, datetime, tzinfo

from sdklib.util.times import timeout, datetime_to_milliseconds_timestamp, seconds_to_milliseconds_timestamp


class GMT1(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        # DST starts last Sunday in March
        d = datetime(dt.year, 4, 1)   # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <=  dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

        def tzname(self,dt):
            return "GMT +1"


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

    def test_seconds_to_milliseconds_timestamp(self):
        res = seconds_to_milliseconds_timestamp(1015801200000)
        self.assertEqual(res, 1015801200000000)
