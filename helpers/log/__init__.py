import socket
import logging
import sys
import os

from logging.handlers import SysLogHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from context_filter import ContextFilter

logging.basicConfig(stream=sys.stdout)
mylogger = logging.getLogger('log')
mylogger.setLevel(logging.INFO)

#...............................................#
# Formatters #

def get_generic_formatter():
	''' returns generic formatting '''
	hostname = socket.gethostname() if socket.gethostname() else socket.getfqdn()
	formatter = logging.Formatter('{0}:%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s'.format(hostname),'%Y-%m-%d %H:%M:%S')
	return formatter

def get_formatter(format_type):
	''' returns formatter respective to format_type '''

	# dynamic formatter function calling
	formatter_mapping ={
		'generic': get_generic_formatter,
	}
	return formatter_mapping[format_type]()

#.................................................#
# Log Handlers #

def add_papertrail_handler(logger, level, config=None, formatter=None):
	''' adding paper trail log handler '''

	# skip if config error
	if not config:
		return

	try:
		log_server = config.get('PAPERTRAIL', 'LOG_SERVER')
		log_port = int(config.get('PAPERTRAIL', 'LOG_PORT'))
	except Exception as ex:
		mylogger.info(\
			'Could not find papertrail config while logger setup...%s'\
			% str(ex))

	syslog_handler = SysLogHandler(address=(log_server, log_port))
	syslog_handler.setLevel(level)
	syslog_handler.setFormatter(formatter) if formatter else None

	logger.addHandler(syslog_handler)

def add_file_handler(logger, level, file_name=None, formatter=None):
	''' adding file handler '''

	if not file_name:
		return

	file_handler = logging.FileHandler(file_name)
	file_handler.setLevel(level)
	file_handler.setFormatter(formatter) if formatter else None

	logger.addHandler(file_handler)

#...........................................................#

def get_logger(app_name='app', config=None, level='INFO', \
	file_name=None, format_type='generic'):
	''' setting up logger '''

	level_mapping = {
		'NOTSET': logging.NOTSET,
		'DEBUG': logging.DEBUG,
		'INFO': logging.INFO,
		'WARNING': logging.WARNING,
		'ERROR': logging.ERROR,
		'CRITICAL': logging.CRITICAL,
	}

	level = level_mapping[level]
	formatter = get_formatter(format_type)

	# getting main logger
	logger = logging.getLogger(app_name)
	logger.setLevel(level)
	logger.addFilter(ContextFilter())

	# adding various subscribers to log stream
	try:
		add_file_handler(logger, level, file_name, formatter=formatter)
		add_papertrail_handler(logger, level, config, formatter=formatter)
	except Exception as ex:
		mylogger.info(\
			'Exception while adding log handler %s' % str(ex))

	return logger