import boto3
import logging
import os
import sys

def upload_to_s3(bucket_name, local_source_path, remote_target_path, is_dir=False):
	''' Uploading given file to s3 bucket

		Parametes :
		-- local_source_path : local path of file or files in directory for input
		-- remote_target_path : remote s3 bucket path of file / directory to store
		-- bucekt_name : name of bucket in s3 that should exist
		-- is_dir : is given local_source path is of directory ? (True / False)
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

