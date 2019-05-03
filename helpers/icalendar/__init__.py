import datetime
import holidays
import os

from bdateutil import relativedelta
from datetime import timedelta

from calendar import monthrange

from pytz import timezone

def get_first_day_of_month():
	''' get first day of month '''

	todayDate = datetime.date.today()

	if todayDate.day > 25:
		todayDate += datetime.timedelta(7)

	first_date = todayDate.replace(day=1)
	return str(first_date)

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

	# adjust month (floor and ceiling check)
	total_months = (dt.month + m) % 12 if dt.month + m > 12 else dt.month + m
	total_months = 1 if total_months < 0 else total_months

	# adjust ceiling
	(fdw, no_of_days) = monthrange(dt.year, dt.month)
	total_days = no_of_days if dt.day + d > no_of_days else dt.day + d

	(ffdw, no_of_days) = monthrange(dt.year + y, total_months)
	total_days = no_of_days if dt.day + d > no_of_days else dt.day + d

	# adjust floor
	total_days = 1 if total_days <= 0 else total_days

	try:
		adjusted_date = datetime.date(dt.year + y, total_months, total_days)
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

def get_period(duration, period, units):
	''' 
		get period
		duration = period in days
		period = period
		units = ( days | months | weeks )
	'''

	end_date = get_today()

	if units == 'days':
		start_date = end_date + relativedelta(bdays=period * duration, holidays=holidays.US())

	elif units == 'months':
		start_date = end_date + relativedelta(bdays=period * 20, holidays=holidays.US())

	elif units == 'weeks':
		start_date = end_date + relativedelta(bdays=period * 5, holidays=holidays.US())

	return str(start_date), str(end_date)
