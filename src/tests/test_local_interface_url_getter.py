"""Unit tests for the LocalInterfaceURLGetter class."""
import os
import json
import shutil
import unittest

from src.main.local_interface_url_getter import LocalInterfaceURLGetter


class TestLocalInterfaceURLGetter(unittest.TestCase):
    """Test cases for the LocalInterfaceURLGetter class."""

    def setUp(self):
        """Set up the test environment."""
        self.source_dir = 'test_source_dir'
        self.excel_file = 'test_excel_file.xlsx'
        self.backup_dir = os.path.join(self.source_dir, 'backup')
        self.error_dir = os.path.join(self.source_dir, 'error')

        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.error_dir, exist_ok=True)

        self.getter = LocalInterfaceURLGetter(self.source_dir, self.excel_file)

    def tearDown(self):
        """Tear down the test environment."""
        shutil.rmtree(self.source_dir)
        if os.path.exists(self.excel_file):
            os.remove(self.excel_file)

    def test_process_json_files_no_json(self):
        """Test process_json_files with no JSON files."""
        self.getter.process_json_files()

        # Verify that an empty DataFrame is created
        self.assertTrue(self.getter.data_frame.isna().all().all())

    def test_process_single_file(self):
        """Test process_single_file with a sample JSON file."""

        # Path to your JSON file
        json_file_path = './src/tests/test_data/interfaces.json'

        # Read the content of the file into a Python dictionary
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            sample_data = json.load(json_file)

        # Write this sample_data to a test file in source_dir
        test_file_path = os.path.join(self.source_dir, 'sample.json')
        with open(test_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(sample_data, json_file)

        self.getter.process_single_file('sample.json')

        # Verify the DataFrame is updated
        # (Assuming self.get_connected_app_name() returns empty string)
        self.assertEqual(
            self.getter.data_frame.loc[0, 'file_name'], 'sample.json')
        self.assertEqual(
            self.getter.data_frame.loc[0, 'body'], json.dumps(sample_data))


if __name__ == '__main__':
    unittest.main()
