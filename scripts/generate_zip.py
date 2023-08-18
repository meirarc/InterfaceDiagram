"""
This module zip the main files in the function.zip
The file need to be upload to a S3 to create the lambda function
"""
import zipfile

with zipfile.ZipFile('./scripts/function.zip', 'a') as zipf:

    zipf.write('src/main/lambda_api_function.py',
               'src/main/lambda_api_function.py')

    zipf.write('src/main/interface_diagram.py',
               'src/main/interface_diagram.py')

    zipf.write('src/main/encoding_helper.py',
               'src/main/encoding_helper.py')

    zipf.write('src/main/json_parser.py',
               'src/main/json_parser.py')

    zipf.write('src/main/config.py',
               'src/main/config.py')

    zipf.write('src/main/local_interface_url_getter.py',
               'src/main/local_interface_url_getter.py')

    zipf.write('src/main/s3_interface_url_getter.py',
               'src/main/s3_interface_url_getter.py')
