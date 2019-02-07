from datetime import datetime 

def is_third_friday(s):
	d = datetime.strptime(s, '%b %d, %Y')
	return d.weekday() == 4 and 14 < d.day < 22
