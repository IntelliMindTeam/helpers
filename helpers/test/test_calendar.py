import datetime
import holidays
import os
import shutil
import sys
import unittest

from bdateutil import relativedelta

from mock import patch, MagicMock, call
from tempfile import mkdtemp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import icalendar

class TestCalendar(unittest.TestCase):
	''' testing calendar module '''

	@patch('icalendar.get_today')
	def test_get_prior_business_day(self, mock_get_today):
		''' To test get prior business day '''

		# yyyy-mm-dd
		input_dates = [
			datetime.date(year=2008, month=1, day=2),	# new year + 1 day
			datetime.date(year=2010, month=12, day=26),	# christmas day + 1 day
			datetime.date(year=2010, month=10, day=15),	# not holiday + 1 day
		]
		expected_dates = [
			'2007-12-31',	# new year - 1 day
			'2010-12-23',	# christmas day - 1 day
			'2010-10-14'	# exact previous day
		]

		mock_get_today.side_effect = input_dates

		response_dates = []
		for _ in range(len(input_dates)):
			res = icalendar.get_prior_business_day()
			response_dates.append(res)

		self.assertEqual(set(response_dates), set(expected_dates))

	@patch('icalendar.get_today')
	def test_adjust_today(self, patched_today):
		''' To test adjusted today date '''

		patched_today.return_value = datetime.date(2019, 5, 3)
		year, month, day = (2, 1, 1)

		expected_date = datetime.date(2021, 6, 4)
		response_date = icalendar.adjust_today(year, month, day)
		self.assertEqual(response_date, expected_date)

		# test case II
		year, month, day = (0, 0, 31)
		expected_date = datetime.date(2019, 5, 31)
		response_date = icalendar.adjust_today(year, month, day)
		self.assertEqual(response_date, expected_date)

		# test case III
		year, month, day = (0, 0, -5)
		expected_date = datetime.date(2019, 5, 1)
		response_date = icalendar.adjust_today(year, month, day)
		self.assertEqual(response_date, expected_date)

		# test case IV
		year, month, day = (0, 15, 0)
		expected_date = datetime.date(2019, 8, 3)
		response_date = icalendar.adjust_today(year, month, day)
		self.assertEqual(response_date, expected_date)

	@patch('icalendar.get_today')
	def test_get_last_business_day(self, patched_today):
		''' To test get last to last business day '''

		# yyyy-mm-dd
		input_dates = [
			datetime.date(year=2008, month=1, day=2),	# new year + 1 day
			datetime.date(year=2010, month=12, day=26),	# christmas day + 1 day
			datetime.date(year=2010, month=10, day=15),	# not holiday + 1 day
		]
		expected_dates = [
			'2007-12-30',	# new year - 2 day
			'2010-12-22',	# christmas day - 2 day
			'2010-10-13'	# previous business day
		]

		patched_today.side_effect = input_dates

		response_dates = []
		for _ in range(len(input_dates)):
			res = icalendar.get_last_business_day()
			response_dates.append(res)

	@patch('icalendar.get_today')
	def test_get_period(self, patched_today):
		''' To test get period '''

		# yyyy-mm-dd
		input_dates = [
			datetime.date(year=2008, month=1, day=2),	# new year + 1 day
			datetime.date(year=2010, month=12, day=26),	# christmas day + 1 day
			datetime.date(year=2010, month=10, day=15),	# not holiday + 1 day
		]

		expected_res = [
			'2008-01-03',
			'2011-01-25',
			'2010-10-29',
		]

		patched_today.side_effect = input_dates

		res = []
		res = [
			icalendar.get_period(1, 1, 'days'),
			icalendar.get_period(1, 1, 'months'),
			icalendar.get_period(1, 2, 'weeks'),
		]

		res = [str(start_date) for start_date, end_date in res]
		self.assertEqual(res, expected_res)
