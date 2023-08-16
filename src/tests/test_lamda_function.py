"""
This module contains tests for the Lambda function.
"""
import json
import unittest
import requests
from bs4 import BeautifulSoup

# Import your lambda_handler function from your script
from src.main.lambda_function import lambda_handler


class TestLambdaFunction(unittest.TestCase):
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


    def test_lamda_handler_response(self):
        """
        Test the draw.io url generate from the lambda function
        """
        # Call the Lambda handler with the test event
        result = lambda_handler(self.test_event, None)
        url = result['body']

        # Perform the GET request
        response = requests.get(url, verify=False, timeout=5)

        # Verify the status code
        self.assertEqual(response.status_code, 200)

        # Use BeautifulSoup to parse the HTML and extract the title
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string

        # Verify the title (replace 'Expected Title' with the expected title value)
        self.assertEqual(title, 'Flowchart Maker & Online Diagram Software')


if __name__ == '__main__':
    unittest.main()
