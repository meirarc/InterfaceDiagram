"""
Module to update the Interface Diagram URL Excel file.

This module contains a class that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.
"""
import os
import json
import shutil
from typing import Dict
import pandas as pd
from openpyxl import load_workbook

from src.main.encoding_helper import EncodingHelper
from src.main.json_parser import JSONParser
from src.main.interface_diagram import InterfaceDiagram

from src.main.data_definitions import SourceStructure
from src.main.excel_utils import create_excel_table

from src.main.logging_utils import debug_logging


class LocalInterfaceURLGetter:
    """
    A class to update the Interface Diagram URL Excel file.

    This class contains methods to load an Excel file, process JSON files to extract
    necessary data, clear existing data in the Excel file, and save new records to the
    Excel file.
    """
    @debug_logging
    def __init__(self, source_dir, excel_file):
        """
        Initializes the LocalInterfaceURLGetter with specified directory paths 
        and an empty DataFrame.
        """

        self.file_info = {
            'source_dir': source_dir,
            'backup_dir': os.path.join(source_dir, 'backup'),
            'error_dir': os.path.join(source_dir, 'error'),
            'excel_file': excel_file,
            'source_path': '',
            'backup_path': '',
            'error_file_path': ''
        }

        self.interfaces = None

        self.data_frame = pd.DataFrame(
            columns=['connected_app', 'body', 'file_name', 'url'])

    @debug_logging
    def process_json_files(self):
        """
        Processes JSON files from the source directory and updates the DataFrame.
        """

        file_control = {'json_files_found': False}

        # Process each file in the source directory
        for filename in os.listdir(self.file_info['source_dir']):
            if filename.endswith('.json'):
                file_control['json_files_found'] = True
                self.process_single_file(filename)

        if not file_control['json_files_found']:
            # Create a new DataFrame with one empty row
            self.data_frame = pd.DataFrame(
                columns=['connected_app', 'body', 'file_name', 'url'], index=[0]
            )

    @debug_logging
    def process_single_file(self, filename: str):
        """
        Processes a single JSON file.
        """
        source_path = os.path.join(self.file_info['source_dir'], filename)
        backup_path = os.path.join(self.file_info['backup_dir'], filename)

        if os.path.exists(backup_path):
            if self.is_content_identical(source_path, backup_path):
                os.remove(source_path)
                return

        try:
            with open(source_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            app_name = self.get_connected_app_name(data)

            self.interfaces = JSONParser.json_to_object(
                [SourceStructure(**item) for item in data])

            diagram = InterfaceDiagram(self.interfaces)
            url = diagram.generate_diagram_url(EncodingHelper())

            self.append_to_data_frame(app_name, data, filename, url)
            shutil.move(source_path, backup_path)

        except KeyError as key_error:
            print(
                f'Error processing file {filename}. Skipping. KeyError: {key_error}')

            error_file_path = os.path.join(
                self.file_info['error_dir'], filename)
            shutil.move(source_path, error_file_path)

    @debug_logging
    def is_content_identical(self, source_path: str, backup_path: str) -> bool:
        """
        Checks if the content of the source file is identical to its backup.
        """
        with open(source_path, 'r', encoding='utf-8') as source_file, \
                open(backup_path, 'r', encoding='utf-8') as backup_file:
            source_content = json.load(source_file)
            backup_content = json.load(backup_file)
        return source_content == backup_content

    @debug_logging
    def get_connected_app_name(self, data: Dict) -> str:
        """
        Extracts the connected app name from the data.
        """
        for item in data:
            if item['app_type'] == 'connected_app':
                return item['app_name']
        return ''

    @debug_logging
    def append_to_data_frame(self, app_name: str, data: Dict, filename: str, url: str):
        """
        Appends a new row to the DataFrame.
        """
        new_index = len(self.data_frame)
        self.data_frame.loc[new_index] = [
            app_name, json.dumps(data), filename, url]

    @debug_logging
    def save_results(self):
        """
        Saves the new records (stored in self.df) to the specified sheet in the Excel file.
        """
        self.data_frame.to_excel(
            self.file_info['excel_file'], index=False, engine='openpyxl')

        work_book = load_workbook(self.file_info['excel_file'])

        create_excel_table(work_book)
        work_book.save(self.file_info['excel_file'])
        work_book.close()
