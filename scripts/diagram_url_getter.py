"""
Module to update the Interface Diagram URL Excel file.

This module contains a class that reads JSON files from a specified directory,
processes the contents of these files, and updates an Excel file with the parsed data.
If no JSON files are found, a blank record is created in the Excel file.
"""
from src.main.interface_url_getter import InterfaceURLGetter

SOURCE_DIR = './diagram/in'
EXCEL_FILE = './diagram/out/interfaces_diagrams_urls.xlsx'

getter = InterfaceURLGetter(SOURCE_DIR, EXCEL_FILE)
getter.process_json_files()
getter.save_results()
