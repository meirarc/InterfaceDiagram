import sys
sys.path.append('.')

from src.main.InterfaceDiagram import InterfaceDiagram
from src.main.JSONParser import JSONParser

import logging
import json

#file_name = 'src/test/test_data/interfaces.json'
file_name = 'diagram/in/backup/app_1CRM.json'

with open(file_name, 'r') as f:
    data = json.load(f)  # Load JSON data from a file

parser = JSONParser()
interfaces = parser.json_to_object(data)

diagram = InterfaceDiagram(data, logging.DEBUG)  # Initialize the InterfaceDiagram with the data
print(diagram.finish())  # Generate the diagram