"""
Lambda Function
"""
import json
import sys

from src.main.s3_interface_url_getter import S3InterfaceURLGetter

sys.path.insert(0, '/var/task/package')


def lambda_handler(event, _):
    """
    Lambda Function
    """
    # Print the event object to CloudWatch Logs
    print("Received event: " + json.dumps(event, indent=2))
    print("sys.path:", sys.path)

    source_dir = 'https://interface-diagram-files.s3.amazonaws.com/in/'
    excel_file = 'https://interface-diagram-files.s3.amazonaws.com/out/interfaces_diagrams_urls.xlsx'

    getter = S3InterfaceURLGetter(source_dir, excel_file)

    getter.process_json_files()
    getter.save_results()

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed files.')
    }
