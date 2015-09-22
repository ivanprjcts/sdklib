import time
import datetime


def get_current_utc(time_format="%Y-%m-%d %H:%M:%S"):
    """
    @return a string representation of the current time in UTC.
    """
    return time.strftime(time_format, time.gmtime())


def today_strf(format="%d/%m/%Y"):
    t = datetime.date.today()
    return t.strftime(format)


def tomorrow_strf(format="%d/%m/%Y"):
    t = datetime.date.today() + datetime.timedelta(days=1)
    return t.strftime(format)


def yesterday_strf(format="%d/%m/%Y"):
    t = datetime.date.today() - datetime.timedelta(days=1)
    return t.strftime(format)


def seconds_to_milliseconds_timestamp(seconds_timestamp):
    return int(round(seconds_timestamp * 1000))


def current_milliseconds_timestamp():
    return seconds_to_milliseconds_timestamp(time.time())


def datetime_to_milliseconds_timestamp(datetime_obj):
    seconds_timestamp = time.mktime(datetime_obj.timetuple())
    return seconds_to_milliseconds_timestamp(seconds_timestamp)
