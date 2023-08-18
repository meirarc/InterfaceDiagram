"""
Module to update the Interface Diagram URL Excel file.

This module contains a class that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.
"""
import io
import json
import os

import pandas as pd

import boto3

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
            'backup_dir': f'{source_dir}backup/',
            'error_dir': f'{source_dir}error',
            'excel_file': excel_file,
            'is_s3': source_dir.startswith('s3://'),
            'source_path': '',
            'backup_path': '',
            'error_file_path': ''
        }

        print('__init__', self.file_info)

        self.parser = JSONParser()
        self.encoder = EncodingHelper()
        self.interfaces = None

        self.data_frame = pd.DataFrame(
            columns=['connected_app', 'body', 'file_name', 'url'])

        if self.file_info['is_s3']:
            self.s3_client = boto3.client('s3')

    def _list_files(self, directory):
        print('_list_files', directory)
        if self.file_info['is_s3']:
            bucket, prefix = self._parse_s3_path(directory)
            result = self.s3_client.list_objects(Bucket=bucket, Prefix=prefix)
            for content in result.get('Contents', []):
                yield content['Key']

    def _read_json(self, filepath):
        print('_read_json', filepath)
        if self.file_info['is_s3']:
            bucket, key = self._parse_s3_path(filepath)
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            return [f.lstrip('in/') for f in pd.read_json(response['Body'])]
        return None

    def _save_to_excel(self, data_frame, filepath):
        print('_save_to_excel', data_frame, filepath)
        if self.file_info['is_s3']:
            excel_buffer = io.BytesIO()
            # Save the DataFrame to the BytesIO object as an Excel file
            data_frame.to_excel(excel_buffer, index=False, engine='openpyxl')

            # Reset the buffer's position to the beginning
            excel_buffer.seek(0)

            # Extract the bucket and key from the S3 filepath
            bucket, key = self._parse_s3_path(filepath)

            # Upload the buffer contents (the Excel file) to S3
            self.s3_client.put_object(
                Bucket=bucket, Key=key, Body=excel_buffer
            )

    def _move_file(self, src_path, dest_path):
        print('_move_file', src_path, dest_path)
        if self.file_info['is_s3']:
            src_bucket, src_key = self._parse_s3_path(src_path)
            dest_bucket, dest_key = self._parse_s3_path(dest_path)
            self.s3_client.copy_object(Bucket=dest_bucket, CopySource={
                                       'Bucket': src_bucket, 'Key': src_key}, Key=dest_key)
            self.s3_client.delete_object(Bucket=src_bucket, Key=src_key)

    def _parse_s3_path(self, path):
        print('_parse_s3_path', path)
        assert path.startswith('s3://')
        path = path[5:]
        bucket, key = path.split('/', 1)

        print('_parse_s3_path', bucket, key)
        return bucket, key

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

        # Loop through files in directory
        for filename in self._list_files(self.file_info['source_dir']):
            if filename.endswith('.json'):

                file_name = filename.lstrip('in/')

                print('process_json_files', file_name)

                # Set the flag to True when a JSON file is found
                file_control['json_files_found'] = True

                # Path to the source file and its potential backup
                self.file_info['source_path'] = os.path.join(
                    self.file_info['source_dir'], file_name)
                self.file_info['backup_path'] = os.path.join(
                    self.file_info['backup_dir'], file_name)

                # Check if the backup file exists and compare the contents
                # Flag to decide whether to process the file or not
                file_control['process_file'] = True

                print('process_json_files', file_control)

                print('process_json_files', self.file_info)
                print('process_json_files', os.path.exists(
                    self.file_info['backup_path']))

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

                print('process_json_files', file_control['process_file'])
                if file_control['process_file']:

                    data = self._read_json(self.file_info['source_path'])
                    # with open(self.file_info['source_path'], 'r', encoding='utf-8') as file:
                    #    data = json.load(file)

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
                        self.data_frame.loc[new_index, 'file_name'] = file_name
                        self.data_frame.loc[new_index, 'url'] = url

                        # Move the successfully processed file to backup
                        # shutil.move(
                        #    self.file_info['source_path'], self.file_info['backup_path'])

                        self._move_file(
                            self.file_info['source_path'], self.file_info['backup_path'])

                    except KeyError as key_error:
                        print(f'Error processing file {file_name}.'
                              f' Skipping. KeyError: {key_error}')

                        self.file_info['error_file_path'] = os.path.join(
                            self.file_info['error_dir'], file_name)

                        # shutil.move(self.file_info['source_path'],
                        #            self.file_info['error_file_path'])

                        self._move_file(
                            self.file_info['source_path'], self.file_info['error_file_path'])
                        continue

        if not file_control['json_files_found']:
            # Create a new DataFrame with one empty row
            self.data_frame = pd.DataFrame(
                columns=['connected_app', 'body', 'file_name', 'url'], index=[0])

    def save_results(self):
        """
        Saves the new records (stored in self.df) to the specified sheet in the Excel file.
        """
        self._save_to_excel(self.data_frame, self.file_info['excel_file'])
