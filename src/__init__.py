# src/utils/__init__.py

from src.cloud_io import MongoIO
from src.constants import MONGO_DATABASE_NAME
from src.exception import CustomException
import os, sys


def fetch_product_names_from_cloud():
    """Fetch product names from MongoDB or local backup"""
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
            db = mongo_io.mongo_ins.db
            
            # List collection names with timeout
            collection_names = db.list_collection_names(maxTimeMS=5000)  # 5 second timeout
            
            # Convert collection names to product names
            product_names = [name.replace('_', ' ') for name in collection_names if name.strip()]
            
            if product_names:
                print(f"Successfully fetched {len(product_names)} products from MongoDB")
            else:
                print("No products found in MongoDB")
                
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
        # Handle MongoDB connection errors
        print(f"Error fetching product names from MongoDB: {e}")
        # Try local backup if MongoDB connection fails
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
