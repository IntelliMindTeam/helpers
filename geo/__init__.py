import pandas as pd

from geopy.geocoders import Nominatim

def get_location(address):
	''' get location '''

	geolocator = Nominatim()
	location = geolocator.geocode(address)
	return {
		'lat': location.latitude,
		'long': location.longitude
	}

def get_country(row):
	''' get country '''

	geolocator = Nominatim()
	hq = row['headquarters']
	location = geolocator.geocode(hq, timeout=10)
	country = location.address.split(",")[-1].strip()
	return pd.Series({'location': country})
