"""
This script is used to create various ZIP files for AWS Lambda functions and layers.
"""
import os
import site
import zipfile
from typing import List, Tuple

# Constants for ZIP file names
API_ZIP = './scripts/lambda_api_function.zip'
S3_NO_PACKAGE_ZIP = './scripts/lambda_s3_function_no_package.zip'
S3_LAYER_ZIP = './scripts/lambda_s3_layer.zip'


def log_file_paths(zipf: zipfile.ZipFile, source_path: str, target_path: str) -> None:
    """
    Log the file paths that are being added to the ZIP file.
    """
    print(
        f"Adding file from {source_path} to {target_path} in the ZIP file {zipf.filename}")


def create_zip(zip_name: str, files_to_zip: List[Tuple[str, str]]) -> None:
    """
    Create a ZIP file and add the specified files.

    Args:
    zip_name (str): Name of the ZIP file to create.
    files_to_zip (List[Tuple[str, str]]): List of source and destination file paths.
    """
    with zipfile.ZipFile(zip_name, 'a') as zipf:
        for src, dest in files_to_zip:
            log_file_paths(zipf, src, dest)
            zipf.write(src, dest)


def create_layer_zip(zip_name: str) -> None:
    """
    Create a ZIP file containing Python packages for a Lambda layer.
    """
    with zipfile.ZipFile(zip_name, 'a') as zipf:
        site_packages_path = site.getsitepackages()[0]
        for root, _, files in os.walk(site_packages_path):
            for file in files:
                src_path = os.path.join(root, file)
                relative_path = os.path.relpath(src_path, site_packages_path)
                dest_path = os.path.join(
                    "python/lib/python3.8/site-packages", relative_path)
                log_file_paths(zipf, src_path, dest_path)
                zipf.write(src_path, dest_path)


def main() -> None:
    """
    Main function to create ZIP files.
    """
    create_zip(
        API_ZIP,
        [
            ('src/main/lambda_api_function.py', 'src/main/lambda_api_function.py'),
            ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
            ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
            ('src/main/json_parser.py', 'src/main/json_parser.py'),
            ('src/main/config.py', 'src/main/config.py')
        ]
    )

    create_zip(
        S3_NO_PACKAGE_ZIP,
        [
            ('src/main/lambda_s3_function.py', 'src/main/lambda_s3_function.py'),
            ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
            ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
            ('src/main/json_parser.py', 'src/main/json_parser.py'),
            ('src/main/config.py', 'src/main/config.py'),
            ('src/main/s3_interface_url_getter.py',
             'src/main/s3_interface_url_getter.py')
        ]
    )

    create_layer_zip(S3_LAYER_ZIP)


if __name__ == '__main__':
    main()


# Creating function_api.zip
# with zipfile.ZipFile('./scripts/lambda_api_function.zip', 'a') as zipf:
#    files_to_zip = [
#        ('src/main/lambda_api_function.py', 'src/main/lambda_api_function.py'),
#        ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
#        ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
#        ('src/main/json_parser.py', 'src/main/json_parser.py'),
#        ('src/main/config.py', 'src/main/config.py')
#    ]#
#
#    for src, dest in files_to_zip:
#        log_file_paths(zipf, src, dest)
#        zipf.write(src, dest)

# Creating function_s3.zip
# with zipfile.ZipFile('./scripts/lambda_s3_function.zip', 'a') as zipf:
#    files_to_zip = [
#        ('src/main/lambda_s3_function.py', 'src/main/lambda_s3_function.py'),
#        ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
#        ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
#        ('src/main/json_parser.py', 'src/main/json_parser.py'),
#        ('src/main/config.py', 'src/main/config.py'),
#        ('src/main/s3_interface_url_getter.py',
#         'src/main/s3_interface_url_getter.py')
#    ]
#
#    for src, dest in files_to_zip:
#        log_file_paths(zipf, src, dest)
#        zipf.write(src, dest)
#
#    # Get the global site-packages directory path
#    site_packages_path = site.getsitepackages()[0]
#
#    # Package the libraries from the global site-packages directory
#    # directly at the root level of the zip file
#    for root, dirs, files in os.walk(site_packages_path):
#        for file in files:
#            src_path = os.path.join(root, file)
#            dest_path = os.path.relpath(
#                os.path.join(root, file), site_packages_path)
#            log_file_paths(zipf, src_path, dest_path)
#            zipf.write(src_path, dest_path)

# Creating function_s3.zip
# with zipfile.ZipFile('./scripts/lambda_s3_function_no_package.zip', 'a') as zipf:
#    files_to_zip = [
#        ('src/main/lambda_s3_function.py', 'src/main/lambda_s3_function.py'),
#        ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
#        ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
#        ('src/main/json_parser.py', 'src/main/json_parser.py'),
#        ('src/main/config.py', 'src/main/config.py'),
#        ('src/main/s3_interface_url_getter.py',
#         'src/main/s3_interface_url_getter.py')
#    ]
#
#    for src, dest in files_to_zip:
#        log_file_paths(zipf, src, dest)
#        zipf.write(src, dest)


# Creating function_s3.zip
# with zipfile.ZipFile('./scripts/lambda_s3_layer.zip', 'a') as zipf:
#    # Get the global site-packages directory path
#    site_packages_path = site.getsitepackages()[0]
#
#    # Package the libraries from the global site-packages directory
#    # directly at the root level of the zip file
#    for root, dirs, files in os.walk(site_packages_path):
#        for file in files:
#            src_path = os.path.join(root, file)
#
#            # Adjust the dest_path to match the Lambda layer directory structure
#            relative_path = os.path.relpath(
#                os.path.join(root, file), site_packages_path)
#
#            dest_path = os.path.join(
#                "python/lib/python3.8/site-packages", relative_path)
#
#            log_file_paths(zipf, src_path, dest_path)
#            zipf.write(src_path, dest_path)
