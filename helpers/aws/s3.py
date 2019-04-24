import boto3
import logging
import os
import sys
import shutil
import datetime
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from log import get_logger
from helpers.exception import exception_handler

logger = get_logger('s3')

def upload_to_s3(bucket_name, local_source_path, remote_target_path,\
	is_dir=False):
	''' Uploading given file or dir to s3 bucket'

		Parameters :

		local_source_path : local path of file or files in directory for input
		remote_target_path : remote s3 bucket path of file / directory to store
		bucekt_name : name of bucket in s3 that should exist
		is_dir : is given local_source path is of directory ? (True / False)
	'''

	client = boto3.client('s3')
	s3 = boto3.resource('s3')

	# Check if bucket already exists
	bucket_exists = False

	try:
		response = client.list_buckets()
	except Exception as ex:
		raise Exception('Can not contact s3 server : {}'.format(ex))

	for bucket in response['Buckets']:
		if bucket['Name'] == bucket_name:
			bucket_exists = True

	if not bucket_exists:
		raise Exception('Given bucket "{}" does not exist'.format(bucket_name))

	# Uploading to s3
	if is_dir:

		# To upload files of given directory
		# Currently aws-s3 sdk does not have api support to upload dir in single call
		for root, dirs, files in os.walk(local_source_path):
			for file_name in files:
				target_final_path = os.path.join(remote_target_path, file_name)
				file_path = os.path.join(root, file_name)

				try:
					s3.meta.client.upload_file(file_path, bucket_name, \
						target_final_path)
				except Exception as ex:
					raise Exception('Error while uploading file - {} :: {}'.format(\
						file_path, ex))

	else:

		# To upload file
		file_name = os.path.split(local_source_path)[-1]
		target_final_path = os.path.join(remote_target_path, file_name)

		try:
			s3.meta.client.upload_file(local_source_path, \
				bucket_name, target_final_path )
		except Exception as ex:
			raise Exception('Error while uploading file - {} :: {}'.format(\
				local_source_path, ex))

@exception_handler([])
def get_sub_dirs(start_date, end_date, source_dir, format):
	''' returns list of sub_directories based on given date range

		source_dir : local source directory path
		format : local sub-directory naming format
		start_date: starting date of sub directory
		end_date:	ending date of sub directory

		sub_directory selection criteria
		(Note: All dates are considered inclusive)

		start_date 	-	end_date

		None 		-		None 		- default today's date
		YYYY-mm-dd	-		None		- start_date to all next
		None 		-		YYYY-mm-dd	- all previous till end_date
		YYYY-mm-dd	-		YYYY-mm-dd  - date range
	'''

	if not (start_date or end_date):
		# default sub_dir as of today's date
		yield datetime.datetime.now().strftime(format)

	elif start_date and (not end_date):

		start_date = datetime.datetime.strptime(start_date, format)

		for sub_dir in sorted(os.listdir(source_dir)):
			if not os.path.isdir(sub_dir): continue
			date = datetime.datetime.strptime(sub_dir, format)
			if date >= start_date: yield date.strftime(format)

	elif (not start_date) and end_date:

		end_date = datetime.datetime.strptime(end_date, format)

		for sub_dir in sorted(os.listdir(source_dir)):
			if not os.path.isdir(sub_dir): continue
			date = datetime.datetime.strptime(sub_dir, format)
			if date <= end_date: yield date.strftime(format)
	else:

		# both dates are given
		start_date = datetime.datetime.strptime(start_date, format)
		end_date = datetime.datetime.strptime(end_date, format)

		for sub_dir in sorted(os.listdir(source_dir)):
			if not os.path.isdir(sub_dir): continue
			date = datetime.datetime.strptime(sub_dir, format)
			if start_date <= date <= end_date: yield date.strftime(format)

@exception_handler()
def backup_to_s3(bucket_name, source_dir, dest_dir, \
	start_date=None, end_date=None, format='%Y-%m-%d', delete_local=False):
	'''
		To create zipped s3-backup of sub-directory
		that has name as todays's date

		Parameters:

		bucket_name : name of the s3-bucket
		source_dir : local source directory path
		dest_dir : remote destination directory path
		format : local sub-directory naming format
		delete_local : deleting local directory after successful upload
		start_date: starting date of sub directory
		end_date:	ending date of sub directory

		sub_directory selection criteria
		(Note: All dates are considered inclusive)

			start_date 	-	end_date

			None 		-		None 		- default today's date
			YYYY-mm-dd	-		None		- start_date to all next
			None 		-		YYYY-mm-dd	- all previous till end_date
			YYYY-mm-dd	-		YYYY-mm-dd  - date range

	'''

	for sub_dir in get_sub_dirs(start_date, end_date, source_dir, format):

		source_dir_path = os.path.join(source_dir, sub_dir)

		# create local archive
		shutil.make_archive(source_dir_path, 'gztar', source_dir_path)
		local_source_path = '{}.tar.gz'.format(source_dir_path)

		# creating remote path
		dir_date = datetime.datetime.strptime(sub_dir, format)

		remote_target_path = os.path.join(
			dest_dir,
			str(dir_date.year),
			str(dir_date.month),
		)
		upload_to_s3(bucket_name, local_source_path, remote_target_path)
		os.remove(local_source_path) # removing zip file

def get_matching_s3_keys(bucket, prefix='', suffix=''):
	"""
	Generate the keys in an S3 bucket.

	Parameters:
	bucket: Name of the S3 bucket.
	prefix: Only fetch keys that start with this prefix (optional).
	suffix: Only fetch keys that end with this suffix (optional).
	"""

	s3_client = boto3.client('s3')

	kwargs = {'Bucket': bucket, 'Prefix': prefix}

	while True:
		resp = s3_client.list_objects_v2(**kwargs)
		for obj in resp['Contents']:
			key = obj['Key']
			if key.endswith(suffix):
				yield key

		try:
			kwargs['ContinuationToken'] = resp['NextContinuationToken']
		except KeyError:
			break

@exception_handler([])
def get_file_paths(remote_source_dir, start_date, end_date,\
	date_format='%Y-%m-%d', suffix='.tar.gz'):
	''' It will yield final file paths '''

	# extracting all dates between given range
	start_date = datetime.datetime.strptime(start_date, date_format).date()
	end_date = datetime.datetime.strptime(end_date, date_format).date()
	days_delta = (end_date - start_date).days

	# creating final remote file_path(key)
	for days in range(0, days_delta + 1):

		date = start_date + datetime.timedelta(days=days)
		file_name = date.strftime(date_format) + suffix

		yield os.path.join(
			remote_source_dir,
			str(date.year),
			str(date.month),
			file_name,
		)

def download_files_by_date_range(bucket_name, remote_source_dir, \
	local_target_dir, start_date, end_date, \
	date_format='%Y-%m-%d', suffix='.tar.gz'):
	''' It will download files from s3 bucket
		by filtering with date-range

		Note :
		* month is assumed to be name as in its integer form
		e.g  for MARCH month directory name should be '3' not 03'

		Params:
		bucket_name :		name of the s3 bucket
		remote_source_dir :	from which dir to find files in s3
		local_target_dir :	local dir path to put downloaded files
		start_date : 		start-date (inclusive)
		end_date : 			end-date (inclusive)
		date_format :		format of file_name convention
							and of string date parameters
	'''

	s3_resouce = boto3.resource('s3')
	bucket = s3_resouce.Bucket(bucket_name)

	kargs = {
		'remote_source_dir': remote_source_dir,
		'start_date': start_date,
		'end_date': end_date,
		'date_format': date_format,
		'suffix': suffix
	}

	for key in get_file_paths(**kargs):

		local_file_path = os.path.join(local_target_dir,\
			os.path.basename(key))

		# download only if file exists else continue
		try:
			logger.info('Checking for key : %s' % str(key))
			bucket.download_file(key, local_file_path)
		except:
			continue

def download_files_by_year(bucket_name, year, remote_source_dir,\
	local_target_dir, suffix='.tar.gz'):
	'''
		download all files in given year dir from s3

		Parametes:
		bucket_name : Name of bucket in s3
		year: name of year dir to be download,
		remote_source_dir : base path of remote s3
		local_target_dir : local base path where to download files
	'''

	s3_resouce = boto3.resource('s3')
	bucket = s3_resouce.Bucket(bucket_name)
	prefix = os.path.join(remote_source_dir, str(year))

	for key in get_matching_s3_keys(bucket_name, prefix=prefix,\
		suffix=suffix):

		local_file_path = os.path.join(local_target_dir, \
			os.path.basename(key))

		# download only if file exists else continue
		try:
			logger.info('Processing key : %s' % str(key))
			bucket.download_file(key, local_file_path)
		except Exception as ex:
			logger.error(ex)
			continue

def create_bucket_name(bucket_prefix):
	''' returns unique bucket_name '''

    # The bucket name must be between 3 and 63 chars long
	return bucket_prefix + str(uuid.uuid4())


def create_bucket(bucket_prefix, s3_connection):
	''' creating new bucket '''

	session = boto3.session.Session()
	current_region = session.region_name
	bucket_name = create_bucket_name(bucket_prefix)

	bucket_response = s3_connection.create_bucket(
		Bucket=bucket_name,
		CreateBucketConfiguration={
		'LocationConstraint': current_region})

	return bucket_name, bucket_response
