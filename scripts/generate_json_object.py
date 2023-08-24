"""
Script for converting a CSV file to a JSON file.
"""
import csv
import json

# Path to the local CSV and JSON file
CSV_FILE = 'src/tests/test_data/interfaces.csv'
JSON_FILE = 'src/tests/test_data/interfaces.json'


def csv_to_json(csv_file_path, json_file_path):
    """
    Converts a CSV file to a JSON file.

    Args:
    csv_file_path (str): The path to the source CSV file.
    json_file_path (str): The path to the destination JSON file.
    """
    # Read the CSV file and convert to a JSON object
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)

    json_data = json.dumps(data, indent=4)

    # Write the json_data to a local file
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    print(f"JSON data has been written to {json_file_path}")


def main():
    """Main function to run the CSV to JSON conversion."""
    csv_to_json(CSV_FILE, JSON_FILE)


if __name__ == '__main__':
    main()
