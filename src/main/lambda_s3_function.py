"""
AWS Lambda Function for Interface URL Getting

This Lambda function processes JSON files from an S3 bucket, generates interface diagram URLs,
and saves the results in an Excel file.
"""
import json
from src.main.s3_interface_url_getter import S3InterfaceURLGetter


def lambda_handler(event, _):
    """
    AWS Lambda Handler function to process JSON files and save results.

    :param event: AWS Lambda event object containing the request details.
    :param _: Context parameter (unused).
    :return: Dictionary containing the response.
    """

    # Log the event object to CloudWatch Logs
    print("Received event: " + json.dumps(event, indent=2))

    # Define source directory and Excel file paths
    source_dir = 's3://interface-diagram-files/in/'
    excel_file = 's3://interface-diagram-files/out/interfaces_diagrams_urls.xlsx'

    # Initialize the S3InterfaceURLGetter class
    getter = S3InterfaceURLGetter(source_dir, excel_file)

    # Process the JSON files and save the results
    getter.process_json_files()
    getter.save_results()

    # Prepare the Lambda function response
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed files.')
    }
