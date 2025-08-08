import pandas as pd
import streamlit as st 
import os
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.utils import fetch_product_names_from_cloud
from src.data_report.generate_data_report import DashboardGenerator

# Initialize MongoDB connection with error handling
try:
    mongo_con = MongoIO()
    if hasattr(mongo_con, 'offline_mode') and mongo_con.offline_mode:
        st.warning("⚠️ Running in offline mode. Some features may be limited.")
        st.info("The application will use locally saved data if available.")
except Exception as e:
    st.error(f"MongoDB Connection Error: {e}")
    st.info("The application will continue in offline mode with limited functionality.")
    # Create a dummy MongoIO instance for offline mode
    class DummyMongoIO:
        def __init__(self):
            self.offline_mode = True
            
        def get_reviews(self, product_name, collection_name=None):
            # Try to load from local backup
            try:
                backup_dir = os.path.join(os.getcwd(), "data_backup")
                backup_file = os.path.join(backup_dir, f"{product_name.replace(' ', '_')}.csv")
                if os.path.exists(backup_file):
                    data = pd.read_csv(backup_file)
                    st.success(f"Loaded {len(data)} reviews from local backup")
                    return data
                else:
                    st.warning(f"No local backup found for {product_name}")
                    return pd.DataFrame()
            except Exception as local_e:
                st.error(f"Error loading reviews from local backup: {local_e}")
                return pd.DataFrame()
    
    mongo_con = DummyMongoIO()


def create_analysis_page(review_data: pd.DataFrame):
    if review_data is not None:

        st.dataframe(review_data)
        if st.button("Generate Analysis"):
            dashboard = DashboardGenerator(review_data)

            # Display general information
            dashboard.display_general_info()

            # Display product-specific sections
            dashboard.display_product_sections()


try:
    # Check if data flag is set in session state
    if st.session_state.get("data", False):
        # Check if product name is set and not empty
        if SESSION_PRODUCT_KEY in st.session_state and st.session_state[SESSION_PRODUCT_KEY].strip():
            try:
                # Get product reviews with error handling
                data = mongo_con.get_reviews(product_name=st.session_state[SESSION_PRODUCT_KEY])
                
                # Check if data is empty (could be due to MongoDB connection issues)
                if data is None or (isinstance(data, pd.DataFrame) and data.empty):
                    st.warning("⚠️ Could not retrieve review data from the database. There might be a connection issue.")
                    st.info("💡 Possible solutions:\n" +
                           "- Check your internet connection\n" +
                           "- Try again later\n" +
                           "- Go back to the search page and re-scrape the reviews")
                    st.markdown(""" # Database Connection Issue""")
                else:
                    create_analysis_page(data)
            except Exception as db_error:
                st.error(f"Database error: {str(db_error)}")
                st.info("💡 The application is having trouble connecting to the database. Please try again later.")
                st.markdown(""" # Database Connection Error""")
        else:
            st.error("Product name is empty. Please go back to the search page and enter a product name.")
            st.markdown(""" # No Product Selected for Analysis""")
    else:
        with st.sidebar:
            st.markdown("""
            No Data Available for analysis. Please Go to search page for analysis.
            """)
except (AttributeError, KeyError) as e:
    st.error(f"Error: {str(e)}")
    st.markdown(""" # No Data Available for analysis.""")
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    st.markdown(""" # Error in Analysis""")
    import traceback
    st.text(traceback.format_exc())

