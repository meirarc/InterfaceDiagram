"""Unit tests for the lambda_handler function."""
import unittest
import json

from src.main.lambda_s3_function import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    """Test cases for the lambda_handler function."""

    def test_lambda_handler(self):
        """Test the lambda_handler function with a sample event."""

        # Prepare a sample event object
        sample_event = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }

        # Execute the Lambda function
        response = lambda_handler(sample_event, None)

        # Validate the response
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(
            response['body']), 'Successfully processed files.')

        # Manual verification steps:
        # 1. Check if the Excel file has been created in the S3 bucket
        # 2. Validate the content of the Excel file
        # Note: These steps should be done manually unless you want to write code to perform these validations


if __name__ == '__main__':
    unittest.main()
