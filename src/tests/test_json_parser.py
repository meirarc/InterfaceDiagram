"""
This module is used to test the JSONParser class and functions
"""
import unittest
from src.main.json_parser import JSONParser

class TestJSONParser(unittest.TestCase):
    """
    This class test the functions of the JSONParser class
    """

    def test_json_to_object(self):
        """
        Test the mock input_data to transform in the expected json object by InterfaceDiagram class
        """
        # Sample input data
        input_data = [
            {
                'code_id': '1',
                'direction': 'Inbound',
                'app_type': 'ERP',
                'app_name': 'SAP',
                'format': 'XML',
                'connection_app': 'CRM',
                'connection_detail': 'Direct',
                'interface_id': '123',
                'interface_url': 'http://example.com'
            }
        ]

        # Expected output data
        expected_output = [
            {
                'code_id': '1',
                'direction': 'Inbound',
                'apps': [
                    {
                        'ERP': 'SAP',
                        'format': 'XML',
                        'connection': {
                            'app': 'CRM',
                            'detail': 'Direct',
                            'interface': {
                                'id': '123',
                                'url': 'http://example.com'
                            }
                        }
                    }
                ]
            }
        ]

        # Call the json_to_object method
        actual_output = JSONParser.json_to_object(input_data)

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)

    def test_parse(self):
        """
        Perform a simple test on to parse a json object
        """
        # Sample JSON string
        json_data = '{"name": "John", "age": 30, "city": "New York"}'

        # Expected Python object
        expected_output = {'name': 'John', 'age': 30, 'city': 'New York'}

        # Create an instance of JSONParser
        parser = JSONParser()

        # Call the parse method
        actual_output = parser.parse(json_data)

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)

# Run the tests
if __name__ == '__main__':
    unittest.main()
