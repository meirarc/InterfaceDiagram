# Interface Diagram - Draw.io

This project provides tools to automatically generate end-to-end (E2E) interface diagrams based on JSON data. It fetches data, processes it, and creates a diagrammatic representation of interfaces using Draw.io.

## Table of Contents

- [Overview](#overview)
- [Features](#Features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project aims to automate the generation of interface diagrams. It includes AWS Lambda functions that process JSON data, convert it to a diagram URL, and then optionally save the URL to an Excel file stored in an S3 bucket.

## Features

- JSON Parsing: Converts JSON data into a structured Python object.
- Diagram Generation: Creates a Draw.io diagram URL based on the processed data.
- Excel File Management: Updates an Excel file with interface diagram URLs.
- AWS Lambda Support: Includes Lambda handlers for seamless integration with AWS.

## Requirements

- Python 3.8
- AWS CLI (for deployment)
- openpyxl (for Excel operations)
- boto3 (for AWS S3 operations)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/meirarc/InterfaceDiagram.git

2. Navigate to the project root:

    ```sh
    cd InterfaceDiagram

3. Install the required packages:
    ```sh
   pip install -r requirements.txt

## Usage
To generate an interface diagram:

1. Place your JSON files in the 'in' folder of your S3 bucket.
2. Run the Lambda handler corresponding to your requirements.

## Directory Structure

- `src/main`: Contains the main application code, including Lambda handlers and utilities for JSON parsing, encoding, and Excel file management.
- `src/test`: Contains test files and test data.
- `scripts`: Contains utility scripts, such as the one for generating the ZIP file for deployment.

## Testing

1. To generate a test JSON object from a CSV, run:
   ```python
   python .\scripts\generate_json_object.py

2. To run the unittest scripts:
    ```python
    python -m unittest discover -s src/tests -p 'test_*.py’

3. To run the Pylint scripts
    ```python
    python3 -m pylint .\src\main

## Deployment
1. Modify the Git Hub action `python_ci_cd.yml` to automatically deploy the project on your AWS account using the cloud formation stack to provision the resources

2. Update the secrets AWS credentials on the Git Action configuration

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.