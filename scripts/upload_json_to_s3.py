import os
import shutil
import boto3

# Set AWS S3 Configurations
s3_bucket = 'interface-diagram-files'
s3_in_dir = 'in/'

# Set local directories
local_in_dir = './diagram/in/'
local_backup_dir = './diagram/in/backup/'

# Initialize boto3 S3 client
s3_client = boto3.client('s3')

# List all files in local 'in' directory
for filename in os.listdir(local_in_dir):
    if filename.endswith('.json'):
        # Full path to the file
        filepath = os.path.join(local_in_dir, filename)

        # Upload file to S3
        s3_client.upload_file(filepath, s3_bucket, s3_in_dir + filename)

        # Move the uploaded file to the backup folder
        shutil.move(filepath, os.path.join(local_backup_dir, filename))

        print(f"Uploaded and moved {filename} to backup.")
