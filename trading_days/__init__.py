import datetime as dt

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
	USMartinLutherKingJr, USPresidentsDay, GoodFriday, USMemorialDay, \
	USLaborDay, USThanksgivingDay


class USTradingCalendar(AbstractHolidayCalendar):
	rules = [
		Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
		USMartinLutherKingJr,
		USPresidentsDay,
		GoodFriday,
		USMemorialDay,
		Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
		USLaborDay,
		USThanksgivingDay,
		Holiday('Christmas', month=12, day=25, observance=nearest_workday)
	]


def get_trading_close_holidays(year):
	''' get trading close holidays '''

	inst = USTradingCalendar()
	return inst.holidays(dt.datetime(year-1, 12, 31), dt.datetime(year, 12, 31))

def is_federal_holiday(today):
    ''' is federal holiday '''

    dr = pd.date_range(start=str(today), end=str(today))
    df = pd.DataFrame()
    df['Date'] = dr

    cal = calendar()
    holidays = cal.holidays(start=dr.min(), end=dr.max())

    df['Holiday'] = df['Date'].isin(holidays)

    result = df.ix[0]['Holiday'] == True
    return result


if __name__ == '__main__':
	print(get_trading_close_holidays(2016))
