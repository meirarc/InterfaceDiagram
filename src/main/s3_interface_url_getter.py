"""
Module to update the Interface Diagram URL Excel file.

This module contains a class that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.
"""
import io
import json

from typing import Dict

import boto3
import pandas as pd
from openpyxl import load_workbook

from src.main.json_parser import JSONParser
from src.main.interface_diagram import InterfaceDiagram

from src.main.data_definitions import SourceStructure

from src.main.excel_utils import create_excel_table

from src.main.logging_utils import debug_logging


class S3InterfaceURLGetter:
    """
    Class to update the Interface Diagram URL Excel file on S3.
    """

    @debug_logging
    def __init__(self, source_dir: str, excel_file: str):
        """
        Initializes with specified S3 directory paths and an empty DataFrame.
        """

        self.file_info = {
            'source_dir': source_dir,
            'backup_dir': f'{source_dir}backup/',
            'error_dir': f'{source_dir}error/',
            'excel_file': excel_file,
            'is_s3': source_dir.startswith('s3://'),
            'source_path': '',
            'backup_path': '',
            'error_file_path': ''
        }

        self.data_frame = pd.DataFrame(
            columns=['connected_app', 'body', 'file_name', 'url'])

        self.interfaces = None

        if self.file_info['is_s3']:
            self.s3_client = boto3.client('s3')

    @debug_logging
    def process_json_files(self):
        """
        Processes JSON files from the S3 source directory and updates the DataFrame.
        """
        if not self.file_info['is_s3']:
            print(f'Not an S3 directory: {self.file_info["source_dir"]}')
            return

        # Initialize a flag to track whether any JSON files are found
        json_files_found = False

        # Process each file in the S3 bucket
        for filename in self._list_files(self.file_info['source_dir']):
            if filename.endswith('.json'):
                json_files_found = True
                self.process_single_file(filename)

        if not json_files_found:
            self.data_frame = pd.DataFrame(
                columns=['connected_app', 'body', 'file_name', 'url'], index=[0]
            )

    @debug_logging
    def process_single_file(self, filename: str):
        """
        Processes a single JSON file from S3.
        """
        clean_file_name = filename.split('/')[-1]

        source_path = f'{self.file_info["source_dir"]}{clean_file_name}'
        backup_path = f'{self.file_info["backup_dir"]}{clean_file_name}'

        if self._compare_files(source_path, backup_path):
            data = self._read_json(source_path)

            # Extract connected_app name from data
            app_name = self.get_connected_app_name(data)

            try:
                self.interfaces = JSONParser.json_to_object(
                    [SourceStructure(**item) for item in data])

                diagram = InterfaceDiagram(self.interfaces)
                url = diagram.generate_diagram_url()

                # Append the new data to the DataFrame
                new_index = len(self.data_frame)
                self.data_frame.loc[new_index] = [
                    app_name, json.dumps(data), clean_file_name, url
                ]
                self._move_file(source_path, backup_path)

            except KeyError as key_error:
                print(f'Error processing file {clean_file_name}.'
                      f'Skipping due to KeyError: {key_error}')

                error_file_path = f'{self.file_info["error_dir"]}{clean_file_name}'
                self._move_file(source_path, error_file_path)

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
    def _list_files(self, directory):
        """
        List the files in a S3 directory
        """
        bucket, prefix = self._parse_s3_path(directory)
        result = self.s3_client.list_objects(Bucket=bucket, Prefix=prefix)

        for content in result.get('Contents', []):
            key = content['Key']
            if not key.startswith('in/backup/') and not key.startswith('in/error/'):
                yield key

    @debug_logging
    def _read_json(self, filepath):
        """
        Read a Json file
        """
        bucket, key = self._parse_s3_path(filepath)
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        json_content = response['Body'].read().decode('utf-8')
        data_frame = pd.read_json(json_content)
        return data_frame.to_dict(orient='records')  # pylint: disable=E1101

    @debug_logging
    def _save_to_excel(self, data_frame, filepath):
        """
        save the data frame to an excel file
        """
        excel_buffer = io.BytesIO()

        # Save the DataFrame to the BytesIO object as an Excel file
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:  # pylint: disable=abstract-class-instantiated
            data_frame.to_excel(writer, index=False)

        # Reset the buffer's position to the beginning
        excel_buffer.seek(0)

        work_book = load_workbook(excel_buffer)
        create_excel_table(work_book)

        # Save the Excel file with the table back to the BytesIO object
        excel_buffer.seek(0)
        work_book.save(excel_buffer)
        work_book.close()

        # Reset the buffer's position to the beginning
        excel_buffer.seek(0)

        # Extract the bucket and key from the S3 filepath
        bucket, key = self._parse_s3_path(filepath)

        # Upload the buffer contents (the Excel file) to S3
        self.s3_client.put_object(
            Bucket=bucket, Key=key, Body=excel_buffer)

    @debug_logging
    def _move_file(self, src_path, dest_path):
        """
        Move the file from a source to destination path in a S3 bucket
        """
        src_bucket, src_key = self._parse_s3_path(src_path)
        dest_bucket, dest_key = self._parse_s3_path(dest_path)

        self.s3_client.copy_object(Bucket=dest_bucket, CopySource={
            'Bucket': src_bucket, 'Key': src_key}, Key=dest_key)
        self.s3_client.delete_object(Bucket=src_bucket, Key=src_key)

    @debug_logging
    def _parse_s3_path(self, path):
        """
        Parse the S3 path into bucket and key
        """
        assert path.startswith('s3://')
        path = path[5:]
        bucket, key = path.split('/', 1)
        return bucket, key.lstrip('/')

    @debug_logging
    def _compare_files(self, source_path, backup_path):
        """
        compare two files on the s3 bucket
        """

        try:
            # Read the source and backup files into pandas DataFrames
            source_content = pd.read_json(self._read_s3_file(source_path))
            backup_content = pd.read_json(self._read_s3_file(backup_path))

            # Compare the content of the two DataFrames
            if source_content.equals(backup_content):  # pylint: disable=no-member
                # If they are identical, delete the source file from S3
                source_bucket, source_key = self._parse_s3_path(source_path)
                self.s3_client.delete_object(
                    Bucket=source_bucket, Key=source_key)
                return False  # Indicate that this file should not be processed further
            return True  # Indicate that this file should be processed further
        except self.s3_client.exceptions.NoSuchKey:
            return True

    @debug_logging
    def _read_s3_file(self, filepath):
        """
        read a file on the s3 bucket
        """
        bucket, key = self._parse_s3_path(filepath)
        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        return file_content

    @debug_logging
    def save_results(self):
        """
        Saves the new records to the specified Excel file in S3.
        """
        if not self.file_info['is_s3']:
            print(f'Not an S3 directory: {self.file_info["excel_file"]}')
            return
        self._save_to_excel(self.data_frame, self.file_info['excel_file'])
