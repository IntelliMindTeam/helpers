import configparser

def read_config(config_file):
	''' read config file '''

	Config = configparser.RawConfigParser()
	Config.read(config_file)

	return Config