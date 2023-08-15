import sys
sys.path.append('.')

from src.main.interface_diagram import InterfaceDiagram
from src.main.json_parser import JSONParser
from src.main.EncodingHelper import EncodingHelper

import logging

#file_name = 'src/tests/test_data/interfaces.json'
file_name = 'diagram/in/backup/app_1CRM.json'

parser = JSONParser()

with open(file_name, 'r') as f:
    data = parser.parse(f.read())

interfaces = parser.json_to_object(data)


diagram = InterfaceDiagram(interfaces, EncodingHelper() ,logging.DEBUG)  # Initialize the InterfaceDiagram with the data
print(diagram.generate_diagram_url())  # Generate the diagram