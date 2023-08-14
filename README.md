# Interface Diagram - Draw.io

This project provides tools to generate a E2E interface diagrams based on data provided. It fetches data, processes it, and generates a diagrammatic representation of interfaces.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

_Briefly explain what the project does and its main features._

## Requirements

- Python 3.x
- AWS CLI (for deployment)

## Setup

1. Clone the repository:
   ```sh
   git clone [repository_url]


2. Navigate to the project root:

    ```sh
    cd InterfaceDiagram

## Directory Structure

- `src/main`: Contains the main application code, including the Lambda handler.
- `src/test`: Contains test files and test data.
- `scripts`: Contains utility scripts, such as the one for generating the ZIP file for deployment.

## Testing

- To generate a test JSON object from a CSV, run:
   
   ```python
   python .\src\test\generate_json_object.py


- To run a local test script:

    ```python
    python .\src\test\test.py

## Deployment
Details about how to deploy the project, especially if there are additional steps or configurations needed.

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
>>>>>>> master
