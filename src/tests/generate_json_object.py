import csv
import json

# Path to the local CSV file
file_path = "src/tests/test_data/interfaces.csv"

# Read the CSV file and convert to a JSON object
with open(file_path, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    data = [row for row in reader]

json_data = json.dumps(data, indent=4)

# Write the json_data to a local file named interfaces.json
with open("src/tests/test_data/interfaces.json", mode='w') as json_file:
    json_file.write(json_data)

print("JSON data has been written to interfaces.json")
