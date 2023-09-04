
## Features

- Periodically fetches data from a public API and stores it as Parquet files.
- Provides RESTful API endpoints for querying and retrieving data.
- Supports filtering data by category and an optional search query.
- Uses Apache Spark for efficient data processing.
- Allows customization of fetch intervals and API URL.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your system.
- Apache Spark installed and configured (if you haven't already).
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) and other dependencies installed (install via `pip`).
- Access to the internet for fetching data from the public API.

## Installation

        Change directory to the project folder:
        cd api-data-processing-app
        pip install -r requirements.txt

## Endpoints
The API provides the following endpoints:

## GET /categories: 
    Retrieve a list of unique categories.
## GET /data/<category>: 
    Retrieve data for a specific category. You can optionally provide a search_query parameter to filter results.


## Configuration
You can configure the app by modifying the app.py file:

api_url: The URL of the public API to fetch data from.
data_path: The path where the data is stored as Parquet files.
fetch_interval_seconds: The interval (in seconds) for periodic data fetching.

## Testing
You can run tests to ensure the functionality of the app. To run tests, use the following command:
    python tests.py


