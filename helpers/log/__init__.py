import socket
import logging
import sys
import os

from logging.handlers import SysLogHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from context_filter import ContextFilter

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

def add_papertrail_log_handler(config, logger, formatter):
	''' adding paper trail log handler '''

	log_server = config.get('PAPERTRAIL', 'LOG_SERVER')
	log_port = int(config.get('PAPERTRAIL', 'LOG_PORT'))

	syslog = SysLogHandler(address=(log_server, log_port))
	syslog.setFormatter(formatter)

	logger.addHandler(syslog)

def get_logger(config, app_name='app', level='INFO', format_type='generic'):
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

	logging.basicConfig(level=level, stream=sys.stdout)

	# getting main logger
	logger = logging.getLogger(app_name)
	logger.setLevel(level)
	logger.addFilter(ContextFilter())

	# adding various subscribers to log stream
	add_papertrail_log_handler(config, logger, formatter)

	return logger