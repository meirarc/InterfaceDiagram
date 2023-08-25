# 1. Delete the actual stack
Write-Host "Deleting current stack..."
aws cloudformation delete-stack --stack-name diagram

# 2. Remove the local file that contains the code of the lambda
Write-Host "Removing local function.zip..."
Remove-Item -Path .\scripts\lambda_api_function.zip
Remove-Item -Path .\scripts\lambda_s3_function_no_package.zip
Remove-Item -Path .\scripts\lambda_s3_layer.zip

# 3. Execute the Python script to generate the function.zip
Write-Host "Generating function.zip..."
python .\scripts\generate_zip.py

# 4. Upload function.zip and lambda_function.yaml to S3
Write-Host "Uploading files to S3..."
aws s3 cp ./scripts/lambda_api_function.zip s3://interface-diagram/lambda_api_function.zip
aws s3 cp ./scripts/lambda_s3_function_no_package.zip s3://interface-diagram/lambda_s3_function.zip
aws s3 cp ./scripts/lambda_s3_layer.zip s3://interface-diagram/lambda_s3_layer.zip
aws s3 cp ./scripts/lambda_function.yaml s3://interface-diagram/lambda_function.yaml

# 5. Wait for the stack to be completely deleted
Write-Host "Waiting for stack deletion..."
Start-Sleep -Seconds 80

# 6. Create the new stack.
Write-Host "Creating new stack..."
aws cloudformation create-stack --stack-name diagram --template-url https://interface-diagram.s3.amazonaws.com/lambda_function.yaml