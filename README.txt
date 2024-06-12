# Website Monitoring Tool

## Description
This is a Python-based website monitoring tool that periodically checks the status of specified websites and logs metrics such as response time, status code, regex match, and error message to a PostgreSQL database.

## Installation
1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Set up a PostgreSQL database and update the connection details in `Config.py`.

## Usage
### Command-Line Interface
    To create the `website_metrics` table in your PostgreSQL database:
        python main.py --create-table
    To start the website monitoring process:
        python main.py