import arctic
import pymongo
import pymysql
from rethinkdb import r
import redis
import pika
import pymongo

from arctic.auth import authenticate

def get_arctic_store(config):
	""" get arctic connection """

	return arctic.Arctic(config.get("MONGODB", "MONGO_SERVER"))


def get_arctic_store_ex(config):
	""" get arctic store """

	store = None
	try:
		conn = pymongo.MongoClient(config.get("MONGODB", "MONGO_SERVER"))

		# authenticate
		auth = authenticate(conn[config.get("MONGODB", "MONGO_DATABASE")],\
								config.get("MONGODB", "MONGO_USER"),\
								config.get("MONGODB", "MONGO_PASSWORD"))
		if auth == True:
			store = arctic.Arctic(conn)

	except Exception as ex:
		print('Exception in getting arctic store {}'.format(str(ex.args)))

	finally:
		return store

def get_mysql_connection(config):
	""" get mysql connection """

	return pymysql.connect(
		host=config.get("MYSQL", "MYSQL_HOST"),
		user=config.get("MYSQL", "MYSQL_USER"),
		password=config.get("MYSQL", "MYSQL_PASSWD"),
		database=config.get("MYSQL", "MYSQL_DATABASE"),
	)


def get_rethink_connection_ex(config):
	""" get rethink db connection  """

	rethink_conn = r.connect(
		host=config.get("RETHINKDB", "RETHINK_HOST"),
		port=config.get("RETHINKDB", "RETHINK_PORT"),
		db=config.get("RETHINKDB", "RETHINK_DB"),
		user=config.get("RETHINKDB", "RETHINK_USER"),
		password=config.get("RETHINKDB", "RETHINK_PASSWORD"),
		timeout=int(config.get("RETHINKDB", "RETHINK_TIMEOUT")),
	)
	return rethink_conn

def get_rethink_connection(config):
	""" get rethink db connection  """

	rethink_conn = r.connect(
		host=config.get("RETHINKDB", "RETHINK_HOST"),
		port=config.get("RETHINKDB", "RETHINK_PORT"),
		db=config.get("RETHINKDB", "RETHINK_DB"),
		user=config.get("RETHINKDB", "RETHINK_USER"),
		password=config.get("RETHINKDB", "RETHINK_PASSWORD"),
		timeout=int(config.get("RETHINKDB", "RETHINK_TIMEOUT")),
	)
	return rethink_conn


def get_redis_connection(config):

	return redis.Redis(
		host=config.get("REDIS", "REDIS_HOST"),
		port=config.get("REDIS", "REDIS_PORT"),
		db=config.get("REDIS", "REDIS_DB"),
	)


def get_rabbit_connection(config):
	credentials = pika.PlainCredentials(
		config.get("RABBIT", "RABBIT_USER"), config.get("RABBIT", "RABBIT_PASSWORD")
	)
	return pika.BlockingConnection(
		pika.ConnectionParameters(
			config.get("RABBIT", "RABBIT_HOST"),
			config.get("RABBIT", "RABBIT_PORT"),
			credentials=credentials,
			heartbeat=config.get("RABBIT", "RABBIT_HEARTBEAT"),
			blocked_connection_timeout=config.get("RABBIT", "RABBIT_TIMEOUT"),
		)
	)


def get_mongo_connection(config):
	return pymongo.MongoClient(
		host=config.get("MONGODB", "MONGO_HOST"),
		port=int(config.get("MONGODB", "MONGO_PORT")),
		username=config.get("MONGODB", "MONGO_USER"),
		password=config.get("MONGODB", "MONGO_PASSWORD"),
		authSource="admin",
		authMechanism="SCRAM-SHA-256",
	)
