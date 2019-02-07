import argparse
import csv
import datetime
import holidays
import os
import json
import hmac
import rethinkdb as r
import configparser

from hashlib import sha1
from lxml import html
from bdateutil import relativedelta
from pytz import timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from connections import get_rethink_connection

def is_empty(path):
	return os.stat(path).st_size==0

def get_lexml(source):
	'''Returns the lxml element of the source'''
	return html.fromstring(source)

def read_config(config_file):
	''' read config file '''

	Config = configparser.ConfigParser()
	Config.read(config_file)

	return Config

def list_files(root_dir):
	return [os.path.join(x[0],y) for x in os.walk(root_dir) for y in x[2]]

def parse_arguments(program_name):
	''' parse arguments '''
	# parse arguments
	parser = argparse.ArgumentParser(description=program_name)
	parser.add_argument('--root_dir', action='store', dest='root_dir',\
		required=True, help='root directory')
	parser.add_argument('--config', action='store', dest='config',\
		required=True, help='config')
	result = parser.parse_args()
	return result

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

def get_newspapers(config):
	''' get list of active newspapers '''
	
	r_conn = get_rethink_connection(config)

	resultset = r.db('socialgraph')\
					.table('newspapers')\
					.filter({'active': 'yes'})\
					.run(r_conn)

	for row in resultset:
		yield row

def read_universe(universe):
	''' get universe '''

	with open(universe, 'r') as univ:
		symbols = json.load(univ)

	symbol_list = [str(x['symbol']) for x in symbols]
	return symbol_list

def generate_hmac_key(secret_shared_key, raw_text):
	''' generate hmac key '''
	
	digest_maker = hmac.new(secret_shared_key, raw_text, sha1)
	return digest_maker.digest().encode("base64").rstrip("\n")

def read_csv_file(file_path):
	with open(file_path) as csv_file:
		csvreader = csv.reader(csv_file)
		for security in csvreader:
			yield security[0]

def read_csv_dict_file(file_path):
	if os.path.isfile(file_path):
		with open(file_path, 'r') as in_file:
			reader = csv.DictReader(in_file)
			for row in reader:
				yield row

def get_rethink_connection(config):
	''' get rethink connection '''

	host = config.get('RETHINKDB', 'RETHINK_HOST')
	port = int(config.get('RETHINKDB', 'RETHINK_PORT'))
	db = config.get('RETHINKDB', 'RETHINK_DB')
	user = config.get('RETHINKDB', 'RETHINK_USER')
	password = config.get('RETHINKDB', 'RETHINK_PASSWORD')
	timeout = int(config.get('RETHINKDB', 'RETHINK_TIMEOUT'))

	return r.connect(host=host, port=port, db=db, user=user, password=password, timeout=timeout)
