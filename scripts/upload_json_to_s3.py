"""
This script uploads JSON files from a local directory to an AWS S3 bucket.
After uploading, it moves the files to a local backup directory.
"""
import os
import shutil
from typing import List

import boto3

# Set AWS S3 Configurations
S3_BUCKET = 'interface-diagram-files'
S3_IN_DIR = 'in/'

# Set local directories
LOCAL_IN_DIR = './diagram/in/'
LOCAL_BACKUP_DIR = './diagram/in/backup/'


def upload_and_move_files(filenames: List[str], s3_client: boto3.client) -> None:
    """
    Upload files to S3 and move them to a local backup directory.

    Args:
    filenames (List[str]): List of filenames to be uploaded and moved.
    s3_client (boto3.client): Initialized boto3 S3 client.
    """
    for filename in filenames:
        if filename.endswith('.json'):
            # Full path to the file
            filepath = os.path.join(LOCAL_IN_DIR, filename)

            # Upload file to S3
            s3_client.upload_file(filepath, S3_BUCKET,
                                  f"{S3_IN_DIR}{filename}")

            # Move the uploaded file to the backup folder
            shutil.move(filepath, os.path.join(LOCAL_BACKUP_DIR, filename))

            print(f"Uploaded and moved {filename} to backup.")


def main() -> None:
    """
    Main function to upload and move files.
    """
    # Initialize boto3 S3 client
    s3_client = boto3.client('s3')

    # List all files in local 'in' directory
    filenames = os.listdir(LOCAL_IN_DIR)

    upload_and_move_files(filenames, s3_client)


if __name__ == '__main__':
    main()
