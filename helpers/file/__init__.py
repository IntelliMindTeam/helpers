import os
import sys
import csv

def list_files(root_dir):
	return [os.path.join(x[0],y) for x in os.walk(root_dir) for y in x[2]]


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


def is_empty(path):
	return os.stat(path).st_size==0
