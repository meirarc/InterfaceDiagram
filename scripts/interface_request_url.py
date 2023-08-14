from src.main.JSONParser import JSONParser

import os
import json
import requests
import pandas as pd

from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo

# Specify directories
source_dir = './diagram/in'
output_dir = './diagram/out'
backup_dir = './diagram/in/backup'
error_dir = './diagram/in/error'


# Define the directory path and the API endpoint
api_endpoint = 'https://gh49irsqq9.execute-api.us-east-1.amazonaws.com/Prod'

# Load the Excel file
excel_file = './diagram/out/interfaces_diagrams_urls.xlsx'


# Read the Excel file using pandas
df = pd.read_excel(excel_file, engine='openpyxl')

# Check if the Table1 is present in the Excel file, if not create it
if 'connected_app' not in df.columns:
    df['connected_app'] = ""

# Loop through files in directory
for filename in os.listdir(source_dir):
    if filename.endswith('.json'):
        with open(os.path.join(source_dir, filename), 'r', encoding='utf-8') as file:
            data = json.load(file)

        app_name = None  # Initialize app_name to None at the beginning of each iteration
        
        # Extract app_name for app_type as 'connected_app'
        for item in data:
            if item['app_type'] == 'connected_app':
                app_name = item['app_name']
                break

        # If app_name is not found, set it to filename
        if app_name is None:
            app_name = ''

        parser = JSONParser()
        interfaces = parser.json_to_object(data)
        
        # POST request to API
        response = requests.post(api_endpoint, json=interfaces)
        
        if response.status_code == 200:
            api_result = response.text  # Assuming the result is plain text
            
            # Add the data to the DataFrame
            new_index = len(df)
            df.loc[new_index, 'connected_app'] = app_name
            df.loc[new_index, 'body'] = json.dumps(data)
            df.loc[new_index, 'file_name'] = filename
            df.loc[new_index, 'url'] = api_result
                
                
# Save the updated DataFrame to the Excel file
df.to_excel(excel_file, index=False, engine='openpyxl')

# Open the Excel file with openpyxl
wb = load_workbook(excel_file)
ws = wb.active

# Define a table and add it to the worksheet
tab = Table(displayName="Table1", ref=ws.dimensions)

# Add a default style to the table
style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                       showLastColumn=False, showRowStripes=True, showColumnStripes=False)
tab.tableStyleInfo = style

ws.add_table(tab)

# Save the Excel file with the table
wb.save(excel_file)
wb.close()
