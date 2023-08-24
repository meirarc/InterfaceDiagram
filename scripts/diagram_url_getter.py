"""
Module to process and update the Interface Diagram URL Excel file.

This module contains a script that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.

Usage: setup a scheduler to run the E2E Flow diagram local or on a server
"""
from src.main.local_interface_url_getter import LocalInterfaceURLGetter

SOURCE_DIR = './diagram/in'
EXCEL_FILE = './diagram/out/interfaces_diagrams_urls.xlsx'

getter = LocalInterfaceURLGetter(SOURCE_DIR, EXCEL_FILE)
getter.process_json_files()
getter.save_results()
