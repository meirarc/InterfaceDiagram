"""
AWS Lambda Function: InterfaceDiagram

This Lambda function handles the generation of an interface diagram URL based on
the input JSON data.
"""
import json
from src.main.data_definitions import SourceStructure
from src.main.json_parser import JSONParser

from src.main.interface_diagram import InterfaceDiagram
from src.main.encoding_helper import EncodingHelper
from src.main.logging_utils import configure_logging


def lambda_handler(event, _):
    """
    AWS Lambda Handler function to generate a diagram URL.

    :param event: AWS Lambda event object containing the request details.
    :param _: Context parameter (unused).
    :return: Dictionary containing the response, including the diagram URL.
    """

    configure_logging()

    encoder = EncodingHelper()
    data = json.loads(event['body'])

    interfaces = JSONParser.json_to_object(
        [SourceStructure(**item) for item in data])

    diagram = InterfaceDiagram(interfaces, encoder)
    url = diagram.generate_diagram_url()

    result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": url
    }

    return result
