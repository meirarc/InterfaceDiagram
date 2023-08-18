"""
Module to update the Interface Diagram URL Excel file.

This module contains a class that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.
"""
import json
import os

import shutil
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl import load_workbook
import pandas as pd

from src.main.encoding_helper import EncodingHelper
from src.main.json_parser import JSONParser
from src.main.interface_diagram import InterfaceDiagram


class S3InterfaceURLGetter:
    """
    A class to update the Interface Diagram URL Excel file.

    This class contains methods to load an Excel file, process JSON files to extract
    necessary data, clear existing data in the Excel file, and save new records to the
    Excel file.
    """

    def __init__(self, source_dir, excel_file):
        """
        Initializes the DiagramURLUpdater with specified directory paths and an empty DataFrame.
        """

        # Specify directories

        self.file_info = {
            'source_dir': source_dir,
            'backup_dir': f'{source_dir}/backup',
            'error_dir': f'{source_dir}/error',
            'excel_file': excel_file,
            'source_path': '',
            'backup_path': '',
            'error_file_path': ''
        }

        self.parser = JSONParser()
        self.encoder = EncodingHelper()
        self.interfaces = None

        self.data_frame = pd.DataFrame(
            columns=['connected_app', 'body', 'file_name', 'url'])

    def process_json_files(self):
        """
        Processes JSON files from the source directory and updates the DataFrame.

        If no JSON files are found in the source directory, a new DataFrame with one
        empty row is created to represent a blank record.
        """
        # Initialize a variable to track whether any JSON files are found
        file_control = {
            'json_files_found': False,
            'process_file': True
        }

        file_control['json_files_found'] = False

        # Loop through files in directory
        for filename in os.listdir(self.file_info['source_dir']):
            if filename.endswith('.json'):

                # Set the flag to True when a JSON file is found
                file_control['json_files_found'] = True

                # Path to the source file and its potential backup
                self.file_info['source_path'] = os.path.join(
                    self.file_info['source_dir'], filename)
                self.file_info['backup_path'] = os.path.join(
                    self.file_info['backup_dir'], filename)

                # Check if the backup file exists and compare the contents
                # Flag to decide whether to process the file or not
                file_control['process_file'] = True

                if os.path.exists(self.file_info['backup_path']):

                    with open(self.file_info['source_path'], 'r',
                              encoding='utf-8') as source_file, \
                            open(self.file_info['backup_path'], 'r',
                                 encoding='utf-8') as backup_file:

                        # Load content of both files
                        source_content = json.load(source_file)
                        backup_content = json.load(backup_file)

                    # If content is identical, don't process the file
                    if source_content == backup_content:
                        file_control['process_file'] = False
                        os.remove(self.file_info['source_path'])

                # If there's no backup or the contents are different, process the source file
                if file_control['process_file']:
                    with open(self.file_info['source_path'], 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Initialize app_name to None at the beginning of each iteration
                    app_name = None

                    # Extract app_name for app_type as 'connected_app'
                    for item in data:
                        if item['app_type'] == 'connected_app':
                            app_name = item['app_name']
                            break

                    # If app_name is not found, set it to filename
                    if app_name is None:
                        app_name = ''

                    # Get the Draw.io URL of the diagram and save it to a file
                    try:
                        self.interfaces = self.parser.json_to_object(data)

                        # Initialize the InterfaceDiagram with the data
                        diagram = InterfaceDiagram(
                            self.interfaces, self.encoder)

                        url = diagram.generate_diagram_url()  # Generate the diagram

                        # Add the data to the DataFrame
                        new_index = len(self.data_frame)
                        self.data_frame.loc[new_index,
                                            'connected_app'] = app_name
                        self.data_frame.loc[new_index,
                                            'body'] = self.parser.dumps(data)
                        self.data_frame.loc[new_index, 'file_name'] = filename
                        self.data_frame.loc[new_index, 'url'] = url

                        # Move the successfully processed file to backup
                        shutil.move(
                            self.file_info['source_path'], self.file_info['backup_path'])

                    except KeyError as key_error:
                        print(f'Error processing file {filename}.'
                              f' Skipping. KeyError: {key_error}')

                        self.file_info['error_file_path'] = os.path.join(
                            self.file_info['error_dir'], filename)

                        shutil.move(self.file_info['source_path'],
                                    self.file_info['error_file_path'])
                        continue

        if not file_control['json_files_found']:
            # Create a new DataFrame with one empty row
            self.data_frame = pd.DataFrame(
                columns=['connected_app', 'body', 'file_name', 'url'], index=[0])

    def save_results(self):
        """
        Saves the new records (stored in self.df) to the specified sheet in the Excel file.
        """
        # Save the processed data back to the Excel file
        self.data_frame.to_excel(
            self.file_info['excel_file'], index=False, engine='openpyxl')

        # Open the Excel file with openpyxl
        work_book = load_workbook(self.file_info['excel_file'])
        work_space = work_book.active

        # Define a table and add it to the worksheet
        tab = Table(displayName="Table1", ref=work_space.dimensions)

        # Add a default style to the table
        style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                               showLastColumn=False, showRowStripes=True, showColumnStripes=False)
        tab.tableStyleInfo = style

        work_space.add_table(tab)

        # Save the Excel file with the table
        work_book.save(self.file_info['excel_file'])
        work_book.close()
