# DAY = first day of current month


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

today = datetime.utcnow().date()

class Intervals:
    DAILY = 'DAILY'
    DAY = 'DAY'
    LAST_WEEK = 'LAST_WEEK'
    PREV_WEEK = 'PREV_WEEK'
    WEEK = 'WEEK'
    TWO_WEEK = 'TWO_WEEK'
    MONTH = 'MONTH'

    ONEOFF = 'ONEOFF'
    FIRST = 'FIRST'
    SECOND = 'SECOND'

intervals = {
    'DAY': datetime.utcnow().date().replace(day=1),
    'WEEK': None
}

class Report:
    def __init__(self):
        self.today = datetime.utcnow().date()

        self.intervals = {
            'LAST_MONTH': self._prev_month,
            'PREV_MONTH': self._prev_month,
            'THIS_MONTH': self._this_month,
        }

    def _prev_week(self):
        pass

    def _prev_month(self):
        """Returns date range from 1st of previous month until final day of previous month."""
        start_date = self.today + relativedelta(months=-1, day=1)
        end_date = self.today + relativedelta(months=-1, day=31)

        return (start_date, end_date)

    def _this_month(self):
        """Returns date range from 1st of current month until current day."""
        start_date = self.today.replace(day=1)
        end_date = self.today

        return (start_date, end_date)


def set_dates(interval=None, start_date=None, end_date=None):
    if interval:
        pass
    elif start_date and end_date:
        pass

class Alpha:
    def hey_report(self):
        print("self: ", self.__dir__())

print(""" hey
            hi there
        yo, sup
        """.replace("\n", ""))
print("done")













"""
# For AltriaUSFacingReport, WEEK means from the 1st til today
if self.interval == 'WEEK':
    end_date = self.current_date
    start_date = end_date.replace(day=1)

# For CCUS_PADE_Report, WEEK means two fridays ago til this friday (today)
elif self.interval == 'WEEK':
    # end_date = self.current_date
    today = datetime.today()
    idx = (today.weekday() + 1) % 7
    end_date = last_thursday = (today - timedelta(idx - 5)) # this seems off
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = (last_thursday - timedelta(14)).strftime("%Y-%m-%d")

# For CoolerScreensAccuracyReport WEEK means a week ago until today
elif self.interval == 'WEEK':
    end_date = self.current_date
    start_date = end_date - timedelta(days=7)

# For CCLibertyUSRedScoreReport WEEK means Sunday to Thursday?
if self.interval == 'WEEK':
	end_date = self.current_date - timedelta(days=self.current_date.isoweekday() - 5)
	start_date = self.current_date - timedelta(days=self.current_date.isoweekday())

# DiageoBeerUSReports, MondelezUSSOSReport is last Sunday to Saturday
elif self.interval == 'WEEK':
    end_date = self.current_date - timedelta(days=self.current_date.isoweekday() + 1)
    start_date = self.current_date - timedelta(days=self.current_date.isoweekday(), weeks=1)

# HeinzCR_Perfect_Store_Report, MondelezUSPSWeeklyReport is Monday til Today
if self.interval == 'WEEK':
    end_date = self.current_date
    start_date = self.current_date - timedelta(days=self.current_date.weekday())

# MondelezDMIUSRawReport ... I dunno, either 8 days ago until 2 days ago or 15 days ago until 3 days ago
if self.interval == 'WEEK':
    vtw_end_date = self.current_date - timedelta(days=2)
    raw_end_date = self.current_date - timedelta(days=3)
    raw_start_date = self.current_date - timedelta(days=15)
    vtw_start_date = self.current_date - timedelta(days=8)

# NESTLEUSSessionCountsReport (this one is my fault) 7 days ago until today
start_date = end_date = self.current_date
if self.interval == 'WEEK':
    start_date = end_date - timedelta(days=7)
"""

"""
# NestleUSAssortmentReport -> yesterday til today
if self.interval == 'LAST_WEEK':
    end_date = self.current_date
    start_date = end_date.replace(day=1)

# NestleUSSOSReport -> 2 sundays ago til last saturday
elif self.interval == 'LAST_WEEK':
    today = self.current_date
    end_date = today - (timedelta(days=today.weekday()) + timedelta(days=2))
    start_date = end_date - (timedelta(days=end_date.weekday()) + timedelta(days=1))

# NestleUSSessionCountsReport -> week before last saturday until saturday
elif self.interval == 'LAST_WEEK':
    today = self.current_date
    end_date = today - (timedelta(days=today.weekday()) + timedelta(days=2))
    start_date = end_date - timedelta(days=7)  # (timedelta(days=end_date.weekday()) + timedelta(days=1))
"""

"""
# HeinzCR_Perfect_Store_Report
elif self.interval == 'PREV_WEEK':
    end_date = self.current_date - timedelta(days=self.current_date.weekday() + 1)
    start_date = end_date - timedelta(days=6)
"""