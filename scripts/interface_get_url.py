import sys
sys.path.append('.')

from src.main.InterfaceDiagram import InterfaceDiagram
from src.main.JSONParser import JSONParser
import json
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
import shutil

# Specify directories
source_dir = './diagram/in'
output_dir = './diagram/out'
backup_dir = './diagram/in/backup'
error_dir = './diagram/in/error'

# Load the Excel file
excel_file = './diagram/out/interfaces_diagrams_urls.xlsx'

# Read the Excel file using pandas
df = pd.read_excel(excel_file, engine='openpyxl')

# Reset the data frame
df = pd.DataFrame(columns=['connected_app', 'body', 'file_name', 'url'])

# Loop through files in directory
for filename in os.listdir(source_dir):
    if filename.endswith('.json'):

        # Path to the source file and its potential backup
        source_path = os.path.join(source_dir, filename)
        backup_path = os.path.join(backup_dir, filename)

        # Check if the backup file exists and compare the contents
        process_file = True  # Flag to decide whether to process the file or not
        

        if os.path.exists(backup_path):
            with open(source_path, 'r', encoding='utf-8') as source_file, \
                 open(backup_path, 'r', encoding='utf-8') as backup_file:
                
                # Load content of both files
                source_content = json.load(source_file)
                backup_content = json.load(backup_file)
                
            # If content is identical, don't process the file
            if source_content == backup_content:
                process_file = False
                os.remove(source_path)
        
        # If there's no backup or the contents are different, process the source file
        if process_file:
            with open(source_path, 'r', encoding='utf-8') as file:
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
                parser = JSONParser()
                interfaces = parser.json_to_object(data)
                diagram = InterfaceDiagram(data)  # Initialize the InterfaceDiagram with the data
                api_result = diagram.finish()  # Generate the diagram

                # Add the data to the DataFrame
                
                new_index = len(df)
                df.loc[new_index, 'connected_app'] = app_name
                df.loc[new_index, 'body'] = json.dumps(data)
                df.loc[new_index, 'file_name'] = filename
                df.loc[new_index, 'url'] = api_result

                # Move the successfully processed file to backup
                shutil.move(source_path, backup_path)

            except KeyError as e:
                print(f"Error processing file {filename}. Skipping. KeyError: {e}")
                error_file_path = os.path.join(error_dir, filename)
                shutil.move(source_path, error_file_path)
                continue

      
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

