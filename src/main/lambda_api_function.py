"""
Lamda Function: InterdaceDiagram
"""
from src.main.interface_diagram import InterfaceDiagram
from src.main.json_parser import JSONParser
from src.main.encoding_helper import EncodingHelper

def lambda_handler(event, _):
    """
    Lambda Handler function
    """
    # Convert the data string into a dictionary
    parser = JSONParser()
    data = parser.parse(event['body'])

    interfaces = parser.json_to_object(data)
    encoder = EncodingHelper()

    diagram = InterfaceDiagram(interfaces, encoder)  # Initialize the InterfaceDiagram with the data
    url = diagram.generate_diagram_url()

    result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { 'Content-Type': 'application/json' },
        "body": url
    }

    return result
