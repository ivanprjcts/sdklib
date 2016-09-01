import time
import datetime
from functools import wraps
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool
import threading
import weakref

from sdklib.compat import thread


thread_pool = None


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


def get_thread_pool():
    global thread_pool
    if thread_pool is None:
        # fix for python <2.7.2
        if not hasattr(threading.current_thread(), "_children"):
            threading.current_thread()._children = weakref.WeakKeyDictionary()
        thread_pool = ThreadPool(processes=1)
    return thread_pool


def timeout(milliseconds=10000, silent=False):
    def wrap_function(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            try:
                async_result = get_thread_pool().apply_async(func, args=args, kwds=kwargs)
                return async_result.get(float(milliseconds) / 1000)
            except thread.error:
                return func(*args, **kwargs)
            except TimeoutError:
                pass

        return __wrapper
    return wrap_function
