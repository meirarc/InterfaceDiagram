"""
This module contains tests for the Lambda function.
"""
import json
import logging

# Import your lambda_handler function from your script
from src.main.interface_diagram import InterfaceDiagram
from src.main.json_parser import JSONParser
from src.main.encoding_helper import EncodingHelper
from src.main.logging_utils import configure_logging
from src.main.data_definitions import SourceStructure


def main():
    """
    Test the lambda_handler function.
    """

    configure_logging(logging.INFO)

    # Call the Lambda handler with the test event
    file_name = 'src/tests/test_data/interfaces.json'

    with open(file_name, 'r', encoding='utf-8') as file_content:
        interface_data = json.load(file_content)

    test_event = {
        "body": json.dumps(interface_data)
    }

    data = json.loads(test_event['body'])

    interfaces = JSONParser.json_to_object(
        [SourceStructure(**item) for item in data])

    # Initialize the InterfaceDiagram class and generate the diagram URL
    diagram = InterfaceDiagram(interfaces)
    url = diagram.generate_diagram_url(EncodingHelper())

    logging.info(url)


if __name__ == '__main__':
    main()
