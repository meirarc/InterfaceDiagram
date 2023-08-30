"""
This module is used to test the JSONParser class and functions
"""
import unittest
import json
from src.main.json_parser import JSONParser
from src.main.data_definitions import SourceStructure, InterfaceStructure, App, Connection, Interface


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
            InterfaceStructure(
                code_id='1',
                direction='Inbound',
                apps=[
                    App(
                        app_type='ERP',
                        app_name='SAP',
                        format='XML',
                        connection=Connection(
                            app='CRM',
                            detail='Direct'),
                        interface=Interface(
                            interface_id='123',
                            interface_url='http://example.com'
                        )
                    )
                ]
            )]

        # Call the json_to_object method
        actual_output = JSONParser.json_to_object(
            [SourceStructure(**item) for item in input_data])

        # Assert that the actual output is equal to the expected output
        self.assertEqual(actual_output, expected_output)


# Run the tests
if __name__ == '__main__':
    unittest.main()
