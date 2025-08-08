import pandas as pd
from src.database_connect import mongo_operation as mongo 
import os, sys
from src.constants import MONGO_DATABASE_NAME
from src.exception import CustomException



class MongoIO:
    mongo_ins = None
    offline_mode = False

    def __init__(self):
        if MongoIO.mongo_ins is None and not MongoIO.offline_mode:
            mongo_db_url = os.getenv("MONGO_DB_URL")
            if not mongo_db_url:
                print("MONGO_DB_URL environment variable not set. Application starting in offline mode.")
                MongoIO.offline_mode = True
                self.mongo_ins = None
                self.offline_mode = True
                return
            
            try:
                MongoIO.mongo_ins = mongo(client_url=mongo_db_url,
                                          database_name=MONGO_DATABASE_NAME)
                print("Successfully connected to MongoDB.")
            except Exception as e:
                print(f"MongoDB connection error: {e}")
                print("Creating offline mode for the application...")
                MongoIO.offline_mode = True
                MongoIO.mongo_ins = None
                
                error_msg = (
                    "Failed to connect to MongoDB. This could be due to one of the following reasons:\n"
                    "1. Your IP address is not whitelisted in MongoDB Atlas\n"
                    "2. Network restrictions or firewall settings\n"
                    "3. VPN interference with SSL connections\n"
                    "4. MongoDB Atlas service might be temporarily unavailable\n"
                    "5. The MONGO_DB_URL environment variable is incorrect.\n\n"
                    "The application will continue in offline mode with limited functionality."
                )
                print(error_msg)
        
        self.mongo_ins = MongoIO.mongo_ins
        self.offline_mode = MongoIO.offline_mode

    def store_reviews(self,
                      product_name: str, reviews: pd.DataFrame):
        try:
            # Check if product_name is empty or None
            if not product_name or product_name.strip() == "":
                raise ValueError("Product name cannot be empty")
                
            # Replace spaces with underscores for collection name
            collection_name = product_name.replace(" ", "_")
            
            # Verify collection name is not empty
            if not collection_name or collection_name.strip() == "":
                raise ValueError("Collection name cannot be empty")
            
            # Check if reviews DataFrame is empty
            if reviews is None or reviews.empty:
                print("Warning: Empty reviews DataFrame provided, nothing to store")
                return
                
            # Check if we're in offline mode
            if self.offline_mode or self.mongo_ins is None:
                print(f"Warning: Operating in offline mode. Reviews for {product_name} will not be stored in MongoDB.")
                # Save to local CSV file as fallback
                try:
                    import os
                    backup_dir = os.path.join(os.getcwd(), "data_backup")
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_file = os.path.join(backup_dir, f"{collection_name}.csv")
                    reviews.to_csv(backup_file, index=False)
                    print(f"Reviews saved locally to {backup_file}")
                    return
                except Exception as local_e:
                    print(f"Error saving reviews locally: {local_e}")
                    return
                
            try:
                # Add timeout handling for MongoDB operations
                self.mongo_ins.bulk_insert(reviews, collection_name)
                print(f"Successfully stored {len(reviews)} reviews for {product_name}")
            except Exception as mongo_error:
                # Handle MongoDB connection errors specifically
                print(f"MongoDB operation error during store_reviews: {mongo_error}")
                print("Failed to store reviews in MongoDB. Attempting to save locally...")
                # Try local backup if MongoDB storage fails
                try:
                    import os
                    backup_dir = os.path.join(os.getcwd(), "data_backup")
                    os.makedirs(backup_dir, exist_ok=True)
                    backup_file = os.path.join(backup_dir, f"{collection_name}.csv")
                    reviews.to_csv(backup_file, index=False)
                    print(f"Reviews saved locally to {backup_file} as fallback")
                except Exception as local_e:
                    print(f"Error saving reviews locally: {local_e}")

        except ValueError as ve:
            # Re-raise validation errors
            raise CustomException(ve, sys)
        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error in store_reviews: {e}")
            raise CustomException(e, sys)

    def get_reviews(self,
                    product_name: str):
        try:
            # Check if product_name is empty or None
            if not product_name or product_name.strip() == "":
                raise ValueError("Product name cannot be empty")
                
            # Replace spaces with underscores for collection name
            collection_name = product_name.replace(" ", "_")
            
            # Verify collection name is not empty
            if not collection_name or collection_name.strip() == "":
                raise ValueError("Collection name cannot be empty")
            
            # Check if we're in offline mode
            if self.offline_mode or self.mongo_ins is None:
                print(f"Warning: Operating in offline mode. Attempting to load reviews from local backup.")
                try:
                    import os
                    backup_dir = os.path.join(os.getcwd(), "data_backup")
                    backup_file = os.path.join(backup_dir, f"{collection_name}.csv")
                    if os.path.exists(backup_file):
                        data = pd.read_csv(backup_file)
                        print(f"Successfully loaded {len(data)} reviews from local backup")
                        return data
                    else:
                        print(f"No local backup found for {product_name}")
                        return pd.DataFrame()
                except Exception as local_e:
                    print(f"Error loading reviews from local backup: {local_e}")
                    return pd.DataFrame()
            
            try:
                # Add timeout handling for MongoDB operations
                data = self.mongo_ins.find(collection_name=collection_name)
                return data
            except Exception as mongo_error:
                # Handle MongoDB connection errors specifically
                print(f"MongoDB operation error: {mongo_error}")
                # Try to load from local backup if MongoDB fails
                try:
                    import os
                    backup_dir = os.path.join(os.getcwd(), "data_backup")
                    backup_file = os.path.join(backup_dir, f"{collection_name}.csv")
                    if os.path.exists(backup_file):
                        data = pd.read_csv(backup_file)
                        print(f"Successfully loaded {len(data)} reviews from local backup")
                        return data
                    else:
                        print(f"No local backup found for {product_name}")
                        return pd.DataFrame()
                except Exception as local_e:
                    print(f"Error loading reviews from local backup: {local_e}")
                    # Return empty DataFrame instead of raising an exception
                    return pd.DataFrame()

        except ValueError as ve:
            # Re-raise validation errors
            raise CustomException(ve, sys)
        except Exception as e:
            # Handle other unexpected errors
            print(f"Unexpected error in get_reviews: {e}")
            raise CustomException(e, sys)
