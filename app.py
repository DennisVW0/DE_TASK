from flask import Flask, request, jsonify
import requests
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, BooleanType
import threading
import logging
import time

app = Flask(__name__)

# Create a SparkSession (Singleton)
spark = SparkSession.builder.appName("APIDataProcessing").getOrCreate()

# Define the schema for the DataFrame
schema = StructType([
    StructField("API", StringType(), True),
    StructField("Description", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Auth", StringType(), True),
    StructField("HTTPS", BooleanType(), True),
    StructField("Cors", StringType(), True),
    StructField("Link", StringType(), True),
])

# Function to fetch and filter data and create a Spark DataFrame
def fetch_and_filter_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()['entries']

        # Filter the data to include only HTTPS links
        filtered_data = [entry for entry in data if entry['HTTPS']]

        # Create a Spark DataFrame from the filtered data
        df = spark.createDataFrame(filtered_data, schema=schema)
        return df
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from the API: {e}")
        return None

# Function to periodically fetch and save data
def periodic_data_fetch_and_save(api_url, interval_seconds, data_path):
    while True:
        df = fetch_and_filter_data(api_url)

        if df:
            # Save the DataFrame as a partitioned Parquet file
            df.write.partitionBy("Category").parquet(data_path, mode="append")
            logging.info(f"Data saved at {time.ctime()}")

        time.sleep(interval_seconds)

# Start a background thread to periodically fetch and save data
api_url = "https://api.publicapis.org/entries"
data_path = "api_data.parquet"
fetch_thread = threading.Thread(target=periodic_data_fetch_and_save, args=(api_url, 12*60*60, data_path))  # Fetch every 12 hours
fetch_thread.daemon = True
fetch_thread.start()

# Endpoint for /categories
@app.route('/categories', methods=['GET'])
def get_categories():
    # Load categories from the saved data file
    df = spark.read.parquet(data_path)
    categories = df.select("Category").distinct().rdd.flatMap(lambda x: x).collect()

    # Return categories as JSON
    return jsonify(categories)

# Endpoint for /data/<category>
@app.route('/data/<category>', methods=['GET'])
def get_data_by_category(category):
    # Load data from the saved data file
    df = spark.read.parquet(data_path)

    # Get the optional search query from the request
    search_query = request.args.get('search_query')

    # Filter data by category
    filtered_df = df.filter(df["Category"] == category)

    # Apply search filter if search_query is provided
    if search_query:
        search_query = search_query.lower()
        filtered_df = filtered_df.filter(
            (df["API"].rlike(search_query)) | (df["Description"].rlike(search_query))
        )

    # Convert the filtered DataFrame to a list of dictionaries
    filtered_data = filtered_df.rdd.map(lambda row: row.asDict()).collect()

    # Return filtered data as JSON
    return jsonify(filtered_data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
