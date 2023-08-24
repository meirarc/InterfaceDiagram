"""
This script downloads an Excel file containing interface diagrams URLs
from an AWS S3 bucket to a local directory.
"""
import os
import boto3

# Set AWS S3 Configurations
S3_BUCKET = 'interface-diagram-files'
S3_OUT_FILE_KEY = 'out/interfaces_diagrams_urls.xlsx'

# Set local directories
LOCAL_OUT_DIR = './diagram/out/'
LOCAL_OUT_FILEPATH = os.path.join(
    LOCAL_OUT_DIR, 'interfaces_diagrams_urls.xlsx')


def main():
    """Main function to download the file from S3."""
    # Initialize boto3 S3 client
    s3_client = boto3.client('s3')

    # Download the Excel file from S3 to local 'out' directory
    s3_client.download_file(S3_BUCKET, S3_OUT_FILE_KEY, LOCAL_OUT_FILEPATH)

    print(f"Downloaded {LOCAL_OUT_FILEPATH} from S3.")


if __name__ == '__main__':
    main()
