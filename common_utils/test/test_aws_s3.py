import os
import shutil
import sys
import unittest

from mock import patch, MagicMock, call
from tempfile import mkdtemp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import aws.s3 as aws_s3

class TestAwsS3(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.list_buckets_response = {
			"Owner": {
				"DisplayName": "name",
				"ID": "EXAMPLE123"
			},
			"Buckets": [{
				"CreationDate": "2016-05-25T16:55:48.000Z",
				"Name": "foo"
			}]
		}
		self.temp_dir = mkdtemp()


	@classmethod
	def tearDownClass(self):
		if os.path.exists(self.temp_dir):
			shutil.rmtree(self.temp_dir)

	@patch('aws.s3.boto3')
	def test_aws_s3_file_and_dir_uploading(self, mock_boto3):
		''' To test aws s3 files uploading works as expected'''

		mock_client = MagicMock()
		mock_client.list_buckets.return_value = self.list_buckets_response

		mock_s3 = MagicMock()

		mock_boto3.client.return_value = mock_client
		mock_boto3.resource.return_value = mock_s3

		bucket_name = self.list_buckets_response['Buckets'][0]['Name']
		local_source_path = '/tmp/abc.txt'
		remote_target_path ='dir/sub_dir'

		file_name = os.path.split(local_source_path)[-1]
		expected_target_path = os.path.join(remote_target_path, file_name)

		aws_s3. upload_to_s3(bucket_name, local_source_path, remote_target_path)

		# testing for file uploading calls
		mock_s3.meta.client.upload_file.assert_called_with( \
			local_source_path, bucket_name, expected_target_path)

		# testing for directory uploading calls
		file1_name = 'abc.txt'
		file2_name = 'xyz.txt'

		file1_path = '{}/{}'.format(self.temp_dir, file1_name)
		file2_path = '{}/{}'.format(self.temp_dir, file2_name)

		os.mknod(file1_path)
		os.mknod(file2_path)

		expected_target_path1 = '{}/{}'.format(remote_target_path, file1_name)
		expected_target_path2 = '{}/{}'.format(remote_target_path, file2_name)

		aws_s3. upload_to_s3(bucket_name, self.temp_dir, remote_target_path, is_dir=True)

		expected_calls = [call(file2_path, bucket_name, expected_target_path2), \
			call(file1_path, bucket_name, expected_target_path1)]

		mock_s3.meta.client.upload_file.assert_has_calls(\
			expected_calls, any_order=True)