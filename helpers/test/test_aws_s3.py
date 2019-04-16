import os
import shutil
import sys
import unittest
import datetime

from mock import patch, MagicMock, call
from tempfile import mkdtemp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../aws')))

from s3 import upload_to_s3
from s3 import backup_to_s3
from s3 import get_file_paths

class TestAwsS3(unittest.TestCase):

	def setUp(self):
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


	def tearDown(self):
		if os.path.exists(self.temp_dir):
			shutil.rmtree(self.temp_dir)

	@patch('s3.boto3')
	def atest_aws_s3_file_and_dir_uploading(self, mock_boto3):
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

		upload_to_s3(bucket_name, local_source_path, remote_target_path)

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

		upload_to_s3(bucket_name, self.temp_dir, remote_target_path, is_dir=True)

		expected_calls = [call(file2_path, bucket_name, expected_target_path2), \
			call(file1_path, bucket_name, expected_target_path1)]

		mock_s3.meta.client.upload_file.assert_has_calls(\
			expected_calls, any_order=True)

	@patch('s3.upload_to_s3')
	def test_backup_to_s3(self, mock_upload_to_s3):
		''' testing backup to s3 capability '''

		# creating today date dir structure

		format = '%Y-%m-%d'
		today = datetime.datetime.now()
		str_today = today.strftime(format)

		sub_dir_name = str_today
		sub_dir_path = os.path.join(self.temp_dir, sub_dir_name)
		os.makedirs(sub_dir_path)

		file_path = os.path.join(sub_dir_path, 'abc.txt')
		open(file_path, 'w').close()

		dest_dir = '/xyz/'
		s3_remote_path = os.path.join(
			dest_dir,
			str(today.year),
			str(today.month)
		)
		bucket_name = 'bucket_name'

		backup_to_s3(bucket_name, self.temp_dir, dest_dir)

		mock_upload_to_s3.assert_called_with(
			bucket_name,
			sub_dir_path + '.tar.gz',
			s3_remote_path,
		)

		#.......................

		# creating past date dir structure
		sub_dir_name = '2018-02-22'
		sub_dir_path = os.path.join(self.temp_dir, sub_dir_name)
		os.makedirs(sub_dir_path)

		file_path = os.path.join(sub_dir_path, 'abc.txt')
		open(file_path, 'w').close()

		dest_dir = '/xyz/'
		remote_path = '/xyz/2018/2'
		bucket_name = 'bucket_name'

		backup_to_s3(bucket_name, self.temp_dir, dest_dir, sub_dir=sub_dir_name)

		mock_upload_to_s3.assert_called_with(
			bucket_name,
			sub_dir_path + '.tar.gz',
			remote_path,
		)

	def test_get_file_paths(self):
		''' To test generation of file paths from date range '''

		kargs = {
			'remote_source_dir': '/test',
			'start_date': '2015-12-30',
			'end_date': '2016-01-1'
		}

		expected_res = [
			'/test/2015/12/2015-12-30.tar.gz',
			'/test/2015/12/2015-12-31.tar.gz',
			'/test/2016/1/2016-01-01.tar.gz'
		]

		res = get_file_paths(**kargs)
		# taking all output at once as it is generator
		res = list(res)
		self.assertEqual(res, expected_res)