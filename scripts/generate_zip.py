import zipfile

with zipfile.ZipFile('./scripts/function.zip', 'a') as zipf:
    zipf.write('src/main/lambda_function.py', 'src/main/lambda_function.py')
    zipf.write('src/main/InterfaceDiagram.py', 'src/main/InterfaceDiagram.py')
    zipf.write('src/main/EncodingHelper.py', 'src/main/EncodingHelper.py')
    zipf.write('src/main/JSONParser.py', 'src/main/JSONParser.py')
