"""
This module zip the main files in the function.zip
The file need to be upload to a S3 to create the lambda function
"""
import zipfile

with zipfile.ZipFile('./scripts/function_api.zip', 'a') as zipf:

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


with zipfile.ZipFile('./scripts/function_s3.zip', 'a') as zipf:

    zipf.write('src/main/lambda_s3_function.py',
               'src/main/lambda_s3_function.py')

    zipf.write('src/main/interface_diagram.py',
               'src/main/interface_diagram.py')

    zipf.write('src/main/encoding_helper.py',
               'src/main/encoding_helper.py')

    zipf.write('src/main/json_parser.py',
               'src/main/json_parser.py')

    zipf.write('src/main/config.py',
               'src/main/config.py')

    zipf.write('src/main/s3_interface_url_getter.py',
               'src/main/s3_interface_url_getter.py')
    
    import os
    for root, dirs, files in os.walk('./.venv/Lib/site-packages'):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.join(root.replace('./.venv/Lib/site-packages', 'package'), file))
