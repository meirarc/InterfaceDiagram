from src.main.InterfaceDiagram import InterfaceDiagram
from src.main.JSONParser import JSONParser
from src.main.EncodingHelper import EncodingHelper

import json

def lambda_handler(event, context):
    # Convert the data string into a dictionary
    data = json.loads(event['body'])


    parser = JSONParser()
    interfaces = parser.json_to_object(data)
    encoder = EncodingHelper()


    diagram = InterfaceDiagram(interfaces, encoder)  # Initialize the InterfaceDiagram with the data
    url = diagram.generate_diagram_url()
    
    print(url)
    
    result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { 'Content-Type': 'application/json' },
        "body": url
    }

    return result
