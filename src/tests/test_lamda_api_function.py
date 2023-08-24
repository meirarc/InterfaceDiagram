"""
This module contains tests for the Lambda function.
"""
import json
import unittest

# Import your lambda_handler function from your script
from src.main.lambda_api_function import lambda_handler


class TestLambdaApiFunction(unittest.TestCase):
    """
    This class contains unit tests for the Lambda function.
    """

    def setUp(self):
        """
        Set up the test case.
        Load the test data from interfaces.json.
        """

        file_name = 'src/tests/test_data/interfaces.json'

        with open(file_name, 'r', encoding='utf-8') as file_content:
            self.interface_data = json.load(file_content)

        self.test_event = {
            "body": json.dumps(self.interface_data)
        }

    def test_lambda_handler(self):
        """
        Test the lambda_handler function.
        """
        # Call the Lambda handler with the test event
        result = lambda_handler(self.test_event, None)

        # Check the result
        # Here, we are checking that the result is a dictionary that contains a statusCode of 200.
        # You can add more assertions based on what your function is expected to return.
        self.assertIsInstance(result, dict)
        self.assertEqual(result['statusCode'], 200)

        # If your function returns a URL in the 'body',
        # you can add an assertion to check that as well
        self.assertIn('http', result['body'])


if __name__ == '__main__':
    unittest.main()
