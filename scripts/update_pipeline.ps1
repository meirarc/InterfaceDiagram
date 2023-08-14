# 1. Delete the actual stack
Write-Host "Deleting current stack..."
aws cloudformation delete-stack --stack-name diagram

# 2. Remove the local file that contains the code of the lambda
Write-Host "Removing local function.zip..."
Remove-Item -Path .\scripts\function.zip

# 3. Execute the Python script to generate the function.zip
Write-Host "Generating function.zip..."
python .\scripts\generate_zip.py

# 4. Upload function.zip and lambda_function.yaml to S3
Write-Host "Uploading files to S3..."
aws s3 cp .\scripts\function.zip s3://interface-diagram/function.zip
aws s3 cp .\scripts\lambda_function.yaml s3://interface-diagram/lambda_function.yaml

# 5. Wait for the stack to be completely deleted
Write-Host "Waiting for stack deletion..."
Start-Sleep -Seconds 10

# 6. Create the new stack
Write-Host "Creating new stack..."
aws cloudformation create-stack --stack-name diagram --template-url https://interface-diagram.s3.amazonaws.com/lambda_function.yaml

# 7. Retrieve the stack output
Write-Host "Waiting for stack creation..."
Start-Sleep -Seconds 20  # Adjust this if you want to wait longer

$stackOutput = aws cloudformation describe-stacks --stack-name diagram --query "Stacks[0].Outputs"
Write-Host $stackOutput
