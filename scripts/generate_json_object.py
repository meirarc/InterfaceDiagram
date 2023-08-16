"""
Script to genetrate the Json file from a CSV file
"""
import csv
import json

# Path to the local CSV and JSON file
CSV_FILE = 'src/tests/test_data/interfaces.csv'
JSON_FILE = 'src/tests/test_data/interfaces.json'

# Read the CSV file and convert to a JSON object
with open(CSV_FILE, mode='r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

json_data = json.dumps(data, indent=4)

# Write the json_data to a local file named interfaces.json
with open(JSON_FILE, mode='w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("JSON data has been written to interfaces.json")
