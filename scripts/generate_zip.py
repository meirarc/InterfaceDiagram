import zipfile

with zipfile.ZipFile('./scripts/function.zip', 'a') as zipf:
    zipf.write('src/main/lambda_function.py', 'src/main/lambda_function.py')
    zipf.write('src/main/interface_diagram.py', 'src/main/interface_diagram.py')
    zipf.write('src/main/EncodingHelper.py', 'src/main/EncodingHelper.py')
    zipf.write('src/main/JSONParser.py', 'src/main/JSONParser.py')
    zipf.write('src/main/config.py', 'src/main/config.py')
