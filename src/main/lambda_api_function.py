"""
AWS Lambda Function: InterfaceDiagram

This Lambda function handles the generation of an interface diagram URL based on
the input JSON data.
"""
from src.main.interface_diagram import InterfaceDiagram
from src.main.json_parser import JSONParser
from src.main.encoding_helper import EncodingHelper


def lambda_handler(event, _):
    """
    AWS Lambda Handler function to generate a diagram URL.

    :param event: AWS Lambda event object containing the request details.
    :param _: Context parameter (unused).
    :return: Dictionary containing the response, including the diagram URL.
    """

    # Initialize JSON parser and EncodingHelper
    parser = JSONParser()
    encoder = EncodingHelper()

    # Parse the JSON data from the event body
    data = parser.parse(event['body'])

    # Convert the parsed data to the required object format
    interfaces = parser.json_to_object(data)

    # Initialize the InterfaceDiagram class and generate the diagram URL
    diagram = InterfaceDiagram(interfaces, encoder)
    url = diagram.generate_diagram_url()

    # Prepare the Lambda function response
    result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": url
    }

    return result
