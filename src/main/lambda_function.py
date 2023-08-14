from src.main.InterfaceDiagram import InterfaceDiagram
import json

def lambda_handler(event, context):
    # Convert the data string into a dictionary
    data = json.loads(event['body'])
    diagram = InterfaceDiagram(data)  # Initialize the InterfaceDiagram with the data
    url = diagram.finish()
    
    print(url)
    
    result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { 'Content-Type': 'application/json' },
        "body": url
    }

    return result
