
"""
Module to test the LocalInterfaceURLGetter
"""
# Import necessary modules
import unittest
import json
import os
import shutil
import tempfile

import pandas as pd
import openpyxl

from src.main.local_interface_url_getter import LocalInterfaceURLGetter

# Create the skeleton of the unittest class


class TestLocalInterfaceURLGetter(unittest.TestCase):
    """
    Class to test the LocalInterfaceURLGetter
    """

    def setUp(self):
        """
        Set up the test environment before each test.
        """

        # Create a temporary directory for the source files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.source_dir = os.path.join(self.temp_dir.name, "test_source_dir")
        self.excel_dir = os.path.join(self.temp_dir.name, "out")

        os.makedirs(self.source_dir, exist_ok=True)

        # Specified input file path
        input_file_path = 'src/tests/test_data/interfaces.json'

        # Create the backup directory as well
        self.backup_dir = os.path.join(self.source_dir, 'backup')
        os.makedirs(self.backup_dir, exist_ok=True)

        # Copy the specified JSON file to the test directory
        file_name = os.path.basename(input_file_path)
        test_file_path = os.path.join(self.source_dir, file_name)
        shutil.copy(input_file_path, test_file_path)

        # Read the JSON data from the file
        with open(test_file_path, 'r', encoding='utf-8') as file_content:
            self.json_files = json.load(file_content)

        # Create a dummy Excel file with some initial data
        self.excel_file_path = os.path.join(
            self.excel_dir, 'test_excel_file.xlsx')

        initial_data = pd.DataFrame([
            {'connected_app': 'InitialApp', 'body': 'InitialBody',
             'file_name': 'InitialFile', 'url': 'InitialURL'}
        ])
        initial_data.to_excel(self.excel_file_path, index=False)

        # Instantiate InterfaceURLGetter
        self.getter = LocalInterfaceURLGetter(
            self.source_dir, self.excel_file_path)

    def tearDown(self):
        """
        Clean up after each test, like deleting any files created during the tests.
        """
        # Remove the temporary directory and all of its contents
        self.temp_dir.cleanup()
        os.remove(self.excel_file_path)

    def test_init(self):
        """
        Test the __init__ method of the InterfaceURLGetter class.
        """
        # Instantiate InterfaceURLGetter
        getter = LocalInterfaceURLGetter(self.source_dir, self.excel_file_path)

        # Assert that the attributes are initialized correctly
        self.assertIsInstance(getter.data_frame, pd.DataFrame)
        self.assertEqual(getter.file_info['source_dir'], self.source_dir)
        self.assertEqual(getter.file_info['excel_file'], self.excel_file_path)

    def test_process_json_files(self):
        """
        Test the process_json_files method of the InterfaceURLGetter class.
        """
        # Call process_json_files
        self.getter.process_json_files()

        # Assert: Check that the actual output has the expected structure

        # Check the shape of the output DataFrame
        self.assertEqual(self.getter.data_frame.shape, (1, 4))

        # Check the column names of the output DataFrame
        expected_columns = ['connected_app', 'body', 'file_name', 'url']
        self.assertListEqual(
            self.getter.data_frame.columns.tolist(), expected_columns)

        # Check that the first row contains some data (i.e., is not empty)
        first_row = self.getter.data_frame.iloc[0]
        self.assertFalse(first_row.isnull().all())

    def test_save_results(self):
        """
        Test the save_results method of the InterfaceURLGetter class.
        """
        # Call save_results
        self.getter.process_json_files()
        self.getter.save_results()

        # Assert: Check that the actual output has the expected structure
        # Load the saved Excel file back into Python
        with pd.ExcelFile(self.excel_file_path) as xls:
            # Load the 'Table1' sheet into a DataFrame
            table1_data = pd.read_excel(xls, 'Sheet1')

        # Check the shape of the output DataFrame
        self.assertEqual(table1_data.shape, (1, 4))

        # Check the column names of the output DataFrame
        expected_columns = ['connected_app', 'body', 'file_name', 'url']
        self.assertListEqual(table1_data.columns.tolist(), expected_columns)

        # Check that the first row contains some data (i.e., is not empty)
        first_row = table1_data.iloc[0]
        self.assertFalse(first_row.isnull().all())

        # Load the saved Excel file back into Python using openpyxl
        work_book = openpyxl.load_workbook(self.excel_file_path)

        # Check that there is a table named 'Table1' in the Excel file
        table_names = [
            table.name for ws in work_book.worksheets for table in ws.tables.values()]
        self.assertIn('Table1', table_names)


# This is just to show that the setUp and tearDown methods are working as expected
# We will write the actual test methods in the next steps
if __name__ == '__main__':
    unittest.main()
