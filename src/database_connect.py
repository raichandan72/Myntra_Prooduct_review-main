# src/database_connect.py

from pymongo import MongoClient
import pandas as pd

class mongo_operation:
    def __init__(self, client_url: str, database_name: str):
        # Configure MongoDB client with modified SSL settings and timeouts
        try:
            # First try with TLS settings
            self.client = MongoClient(
                client_url,
                tls=True,
                tlsAllowInvalidCertificates=True,  # Disable certificate verification for troubleshooting
                connectTimeoutMS=30000,     # Increase connection timeout to 30 seconds
                socketTimeoutMS=30000,      # Increase socket timeout to 30 seconds
                serverSelectionTimeoutMS=30000  # Increase server selection timeout
            )
        except Exception as e:
            print(f"First connection attempt failed: {e}")
            # Fall back to older SSL settings if TLS fails
            self.client = MongoClient(
                client_url,
                ssl=True,
                ssl_cert_reqs='CERT_NONE',  # Disable certificate verification for troubleshooting
                connectTimeoutMS=30000,     # Increase connection timeout to 30 seconds
                socketTimeoutMS=30000,      # Increase socket timeout to 30 seconds
                serverSelectionTimeoutMS=30000  # Increase server selection timeout
            )
        self.db = self.client[database_name]

    def bulk_insert(self, df: pd.DataFrame, collection_name: str):
        # Validate collection name
        if not collection_name or collection_name.strip() == "":
            raise ValueError("Collection name cannot be empty")
        records = df.to_dict(orient="records")
        self.db[collection_name].insert_many(records)

    def find(self, collection_name: str):
        # Validate collection name
        if not collection_name or collection_name.strip() == "":
            raise ValueError("Collection name cannot be empty")
        return list(self.db[collection_name].find({}, {'_id': False}))
