import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string from environment variables
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {MONGO_DB_URL}")

# Certificate for secure connection
ca = certifi.where()

# Custom exception and logging imports
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json(self, file_path):
        """
        Converts a CSV file to a JSON-like dictionary.
        """
        try:
            # Read CSV file into a DataFrame
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)

            # Convert DataFrame to a list of dictionaries (records)
            records = data.to_dict(orient="records")

            if not records:
                raise ValueError("The CSV file is empty or improperly formatted.")

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        """
        Inserts records into the specified MongoDB collection.
        """
        try:
            # Validate that records is a non-empty list
            if not isinstance(records, list) or not records:
                raise TypeError("The 'records' argument must be a non-empty list.")

            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

            # Access the specified database and collection
            db = self.mongo_client[database]
            collection = db[collection]

            # Insert records into the collection
            result = collection.insert_many(records)

            # Return the count of inserted records
            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        # File path and MongoDB configuration
        FILE_PATH = "Network_Data/phisingData.csv"
        DATABASE = "FARHANJHV"
        COLLECTION = "NetworkData"

        # Instantiate the class
        networkobj = NetworkDataExtract()

        # Convert CSV to JSON-like records
        records = networkobj.csv_to_json(file_path=FILE_PATH)
        print(f"Records extracted: {len(records)}")

        # Insert data into MongoDB
        no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"Number of records inserted into MongoDB: {no_of_records}")

    except Exception as e:
        print(f"An error occurred: {e}")
