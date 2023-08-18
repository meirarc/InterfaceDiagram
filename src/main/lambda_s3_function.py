"""
Lambda Function
"""

from src.main.s3_interface_url_getter import S3InterfaceURLGetter
import sys
import json


def lambda_handler(event, _):
    """
    Lambda Function
    """
    # Print the event object to CloudWatch Logs
    print("Received event: " + json.dumps(event, indent=2))

    source_dir = 'https://interface-diagram-files.s3.amazonaws.com/in/'
    excel_file = 'https://interface-diagram-files.s3.amazonaws.com/out/interfaces_diagrams_urls.xlsx'

    getter = S3InterfaceURLGetter(source_dir, excel_file)

    getter.process_json_files()
    getter.save_results()

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed files.')
    }
