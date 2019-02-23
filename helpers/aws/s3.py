import boto3
import logging
import os
import sys
import shutil
import datetime

def upload_to_s3(bucket_name, local_source_path, remote_target_path, is_dir=False):
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

def backup_to_s3(bucket_name, source_dir, dest_dir, format='%Y-%m-%d', sub_dir=None):
	'''
		To create zipped s3-backup of sub-directory that has name as todays's date

		Parameters:

		bucket_name : name of the s3-bucket
		source_dir : local source directory path
		dest_dir : remote destination directory path
		format : local sub-directory naming format
		sub_dir	: sub-directory to be zipped 
				  (default sub_dir will be of today's date name)

	'''

	if not sub_dir:
		# default sub_dir as of today's date
		try:
			sub_dir = datetime.datetime.now().strftime(format)
		except:
			raise Exception('invalid date-format')

	source_dir_path = os.path.join(source_dir, sub_dir)
	if not os.path.exists(source_dir_path):
		return

	# create local archive
	shutil.make_archive(source_dir_path, 'zip', source_dir_path)
	local_source_path = '{}.zip'.format(source_dir_path)

	# creating remote path
	try:
		dir_date = datetime.datetime.strptime(sub_dir, format)
	except:
		raise Exception('invalid date formate of sub-directory')

	remote_target_path = os.path.join(
		dest_dir,
		str(dir_date.year),
		str(dir_date.month),
	)

	upload_to_s3(bucket_name, local_source_path, remote_target_path)

	# removing zip file
	os.remove(local_source_path)