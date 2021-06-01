import datetime
import calendar

import pytz

class DateFilter():
    def __init__(self, tz='Asia/Shanghai'):
        self.tz = pytz.timezone(tz)

    def _is_date_in_range(self, date, left, right):
        return date >= left and date < right, date < left

    def today(self, date):
        # pubdate [lt, gt)
        now = datetime.datetime.now(tz=self.tz).replace(tzinfo=None)
        today = datetime.datetime(now.year, now.month, now.day)
        tomorrow = today + datetime.timedelta(1)

        return self._is_date_in_range(date, today, tomorrow)

    def yesterday(self, date):
        now = datetime.datetime.now(tz=self.tz).replace(tzinfo=None)
        # 这里的时间是今天的 0:0:0 开始算的
        today = datetime.datetime(now.year, now.month, now.day)
        yesterday = today - datetime.timedelta(1)

        return self._is_date_in_range(date, yesterday, today)

    def month(self, date, year, month):
        monthrange = calendar.monthrange(year, month)[1]

        curr_month = datetime.datetime(year, month, 1)
        next_month = datetime.timedelta(1) + datetime.datetime(year, month, monthrange)

        return self._is_date_in_range(date, curr_month, next_month)

    def specified_date(self, date, lyear, lmonth, lday, ryear, rmonth, rday):
        left = datetime.datetime(lyear, lmonth, lday)
        right = datetime.datetime(ryear, rmonth, rday) + datetime.timedelta(1)

        return self._is_date_in_range(date, left, right)
