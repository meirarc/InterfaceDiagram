
import zipfile
import os
import site

# Function to log the paths that are being added to the zip file


def log_file_paths(zipf, source_path, target_path):
    print(
        f"Adding file from {source_path} to {target_path} in the zip file {zipf.filename}")


# Creating function_api.zip
with zipfile.ZipFile('./scripts/function_api.zip', 'a') as zipf:
    files_to_zip = [
        ('src/main/lambda_api_function.py', 'src/main/lambda_api_function.py'),
        ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
        ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
        ('src/main/json_parser.py', 'src/main/json_parser.py'),
        ('src/main/config.py', 'src/main/config.py')
    ]

    for src, dest in files_to_zip:
        log_file_paths(zipf, src, dest)
        zipf.write(src, dest)

# Creating function_s3.zip
with zipfile.ZipFile('./scripts/function_s3.zip', 'a') as zipf:
    files_to_zip = [
        ('src/main/lambda_s3_function.py', 'src/main/lambda_s3_function.py'),
        ('src/main/interface_diagram.py', 'src/main/interface_diagram.py'),
        ('src/main/encoding_helper.py', 'src/main/encoding_helper.py'),
        ('src/main/json_parser.py', 'src/main/json_parser.py'),
        ('src/main/config.py', 'src/main/config.py'),
        ('src/main/s3_interface_url_getter.py',
         'src/main/s3_interface_url_getter.py')
    ]

    for src, dest in files_to_zip:
        log_file_paths(zipf, src, dest)
        zipf.write(src, dest)

    # Get the global site-packages directory path
    site_packages_path = site.getsitepackages()[0]

    # Package the libraries from the global site-packages directory
    for root, dirs, files in os.walk(site_packages_path):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(root.replace(
                site_packages_path, 'package'), file)
            log_file_paths(zipf, src_path, dest_path)
            zipf.write(src_path, dest_path)
