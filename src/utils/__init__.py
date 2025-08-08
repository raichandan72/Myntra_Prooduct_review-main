from src.cloud_io import MongoIO
import pandas as pd
from typing import List


def fetch_product_names_from_cloud() -> List[str]:
    """
    Fetches the list of product names from MongoDB by retrieving all collection names
    and converting them back to product names (replacing underscores with spaces).
    Falls back to local backup if MongoDB is unavailable or in offline mode.
    
    Returns:
        List[str]: A list of product names stored in the database or local backup
    """
    try:
        # Initialize MongoDB connection
        mongo_io = MongoIO()
        
        # Check if we're in offline mode
        if hasattr(mongo_io, 'offline_mode') and mongo_io.offline_mode or mongo_io.mongo_ins is None:
            print("Operating in offline mode. Attempting to fetch product names from local backup.")
            try:
                import os
                backup_dir = os.path.join(os.getcwd(), "data_backup")
                if os.path.exists(backup_dir):
                    # Get CSV files from backup directory
                    product_names = [f.replace('.csv', '') for f in os.listdir(backup_dir) if f.endswith('.csv')]
                    if product_names:
                        print(f"Found {len(product_names)} products in local backup")
                        return product_names
                    else:
                        print("No products found in local backup")
                        return []
                else:
                    print("No local backup directory found")
                    return []
            except Exception as local_e:
                print(f"Error fetching product names from local backup: {local_e}")
                return []
        
        # Try MongoDB connection
        try:
            # Access the MongoDB client directly
            client = mongo_io.mongo_ins.client
            # Get the database
            db = mongo_io.mongo_ins.db
            
            # Set a timeout for the list_collection_names operation
            collections = db.list_collection_names(maxTimeMS=5000)  # 5 second timeout
            
            # Convert collection names back to product names (replace underscores with spaces)
            # Filter out any empty product names to prevent errors
            product_names = [collection.replace('_', ' ') for collection in collections if collection.strip()]
            
            print(f"Successfully fetched {len(product_names)} product names from database")
            return product_names
            
        except Exception as mongo_error:
            # Handle MongoDB connection errors specifically
            print(f"MongoDB connection error in fetch_product_names_from_cloud: {mongo_error}")
            print("Unable to connect to MongoDB. Trying local backup.")
            
            # Try local backup if MongoDB fails
            try:
                import os
                backup_dir = os.path.join(os.getcwd(), "data_backup")
                if os.path.exists(backup_dir):
                    # Get CSV files from backup directory
                    product_names = [f.replace('.csv', '') for f in os.listdir(backup_dir) if f.endswith('.csv')]
                    if product_names:
                        print(f"Found {len(product_names)} products in local backup")
                        return product_names
                    else:
                        print("No products found in local backup")
                        return []
                else:
                    print("No local backup directory found")
                    return []
            except Exception as local_e:
                print(f"Error fetching product names from local backup: {local_e}")
                return []
            
    except Exception as e:
        print(f"Unexpected error fetching product names: {e}")
        return []