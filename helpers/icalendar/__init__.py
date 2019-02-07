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
