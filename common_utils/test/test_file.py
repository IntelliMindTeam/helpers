import os
import shutil
import sys
import unittest

from mock import patch, MagicMock, call
from tempfile import mkdtemp

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import file

class TestUtils(unittest.TestCase):
	''' testing utils '''

	def setUp(self):
		self.temp_dir = mkdtemp()

	def tearDown(self):
		if os.path.exists(self.temp_dir):
			shutil.rmtree(self.temp_dir)

	def test_listing_of_all_dir_files_in_recursive(self):
		''' To test that it list all file path recursive '''

		# creating dir_structure to test
		# temp_dir |
		# 		   |-> a.txt
		#		   |-> b -> b.txt

		file1_path = '{}/{}'.format(self.temp_dir, 'a.txt')
		dir_path = '{}/{}'.format(self.temp_dir, 'b')
		os.mkdir(dir_path)
		file2_path = '{}/{}'.format(dir_path, 'b.txt')
		open(file1_path, 'w').close()
		open(file2_path, 'w').close()

		expected_file_list = [file1_path, file2_path]

		response_file_list = file.list_files(self.temp_dir)

		self.assertEqual(set(expected_file_list), set(response_file_list))
