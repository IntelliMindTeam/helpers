import arctic
import pymysql
import rethinkdb as r

#from influxdb.influxdb08 import DataFrameClient
from influxdb import DataFrameClient

def get_arctic_store(config):
	''' get arctic connection '''

	return arctic.Arctic(config.get('MONGODB', 'MONGO_SERVER'))

def get_mysql_connection(config):
    ''' get mysql connection '''

    return pymysql.connect(host=config.get('MYSQL', 'MYSQL_HOST'),
                            user=config.get('MYSQL', 'MYSQL_USER'),
                            passwd=config.get('MYSQL', 'MYSQL_PASSWD'),
                            db=config.get('MYSQL', 'MYSQL_DATABASE'))

def get_rethink_connection(props):
	''' get rethink db connection  '''

	rethink_conn = r.connect(host=props.get('RETHINKDB', 'RETHINK_HOST'),\
								port=props.get('RETHINKDB', 'RETHINK_PORT'),\
								db=props.get('RETHINKDB', 'RETHINK_DB'),\
								user=props.get('RETHINKDB', 'RETHINK_USER'),\
								password=props.get('RETHINKDB', 'RETHINK_PASSWORD'),\
								timeout=int(props.get('RETHINKDB', 'RETHINK_TIMEOUT')))
	return rethink_conn

def get_dataframe_client(props):
	''' get influx db connection '''

	user = props.get('INFLUXDB', 'INFLUX_USERNAME')
	password = props.get('INFLUXDB', 'INFLUX_PASSWORD')
	host = props.get('INFLUXDB', 'INFLUX_SERVER')
	port = props.get('INFLUXDB', 'INFLUX_PORT')
	dbname = props.get('INFLUXDB', 'INFLUX_DATABASE')

	return DataFrameClient(host, port, user, password, dbname)

def get_dataframe_hist_client(props):
	''' get influx db connection '''

	user = props.get('INFLUXDB', 'INFLUX_USERNAME')
	password = props.get('INFLUXDB', 'INFLUX_PASSWORD')
	host = props.get('INFLUXDB', 'INFLUX_SERVER')
	port = props.get('INFLUXDB', 'INFLUX_PORT')
	dbname = props.get('INFLUXDB', 'HISTORICAL_DB')

	return DataFrameClient(host, port, user, password, dbname)
