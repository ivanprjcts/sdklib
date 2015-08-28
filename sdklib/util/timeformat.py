import datetime
from decorators import deprecated


@deprecated
def today_strf():
    t = datetime.date.today()
    return t.strftime("%d/%m/%Y")


@deprecated
def tomorrow_strf():
    t = datetime.date.today() + datetime.timedelta(days=1)
    return t.strftime("%d/%m/%Y")


@deprecated
def yesterday_strf():
    t = datetime.date.today() - datetime.timedelta(days=1)
    return t.strftime("%d/%m/%Y")