import datetime
import holidays
import os

from bdateutil import relativedelta

from pytz import timezone

def get_today():
	''' get today '''

	now_time = datetime.datetime.now(timezone('US/Eastern'))
	return now_time.date()

def get_prior_business_day():
	''' get latest business day '''

	today = get_today()
	prior_day = today + relativedelta(bdays=-1,  holidays=holidays.US())
	return str(prior_day)

def adjust_today(y, m, d):
	''' adjust date according to offset '''

	# get today's date
	dt = get_today()

	# adjust according to delta
	try:
		adjusted_date = datetime.date(dt.year + y, dt.month + m , dt.day + d)
	except:
		raise Exception('invalid offset')	

	return adjusted_date


def get_duration_in_weeks_from_dt(duration, end_date):
	''' get start, end date for a week '''

	today = end_date
	no_of_days = duration * 5 if duration > 0 else 2
	end_day = today + relativedelta(bdays=-1,  holidays=holidays.US())
	start_day = today + relativedelta(bdays=-1 * no_of_days,  holidays=holidays.US())
	return (str(start_day), str(end_day))

def get_duration_in_weeks(duration):
	''' get start, end date for a week '''

	today = get_today()
	no_of_days = duration * 5 if duration > 0 else 2
	end_day = today + relativedelta(bdays=-1,  holidays=holidays.US())
	start_day = today + relativedelta(bdays=-1 * no_of_days,  holidays=holidays.US())
	return (str(start_day), str(end_day))

def get_last_business_day():
	''' get last business day '''

	today = get_today()
	prior_day = today + relativedelta(bdays=-2,  holidays=holidays.US())
	return str(prior_day)
