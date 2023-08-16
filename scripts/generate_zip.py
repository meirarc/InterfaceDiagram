import zipfile

with zipfile.ZipFile('./scripts/function.zip', 'a') as zipf:
    zipf.write('src/main/lambda_function.py', 'src/main/lambda_function.py')
    zipf.write('src/main/interface_diagram.py', 'src/main/interface_diagram.py')
    zipf.write('src/main/encoding_helper.py', 'src/main/encoding_helper.py')
    zipf.write('src/main/json_parser.py', 'src/main/json_parser.py')
    zipf.write('src/main/config.py', 'src/main/config.py')
