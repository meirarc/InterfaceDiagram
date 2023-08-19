import os
import boto3

# Set AWS S3 Configurations
s3_bucket = 'interface-diagram-files'
s3_out_file_key = 'out/interfaces_diagrams_urls.xlsx'

# Set local directories
local_out_dir = './diagram/out/'
local_out_filepath = os.path.join(
    local_out_dir, 'interfaces_diagrams_urls.xlsx')

# Initialize boto3 S3 client
s3_client = boto3.client('s3')

# Download the Excel file from S3 to local 'out' directory
s3_client.download_file(s3_bucket, s3_out_file_key, local_out_filepath)

print(f"Downloaded {local_out_filepath} from S3.")
