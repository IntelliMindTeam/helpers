import datetime
import os
import sys
import unittest

from mock import patch, MagicMock, call

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import icalendar.options as options

class TestCalendar(unittest.TestCase):
	''' testing calendar module '''

	def test_is_third_friday(self):
		''' To test is given date is on third friday'''

		input_dates = {
			('Feb 15, 2019', True),
			('Feb 17, 2019', False),
			('Jan 19, 2018', True),
			('Jan 18, 2018', False),
		}

		for date, is_third_friday in input_dates:
			self.assertEqual(options.is_third_friday(date), is_third_friday)