import pandas as pd
import streamlit as st 
from dotenv import load_dotenv
from src.cloud_io import MongoIO
from src.constants import SESSION_PRODUCT_KEY
from src.scrapper.scrape import ScrapeReviews

# Load environment variables from .env file
load_dotenv()

# Initialize MongoDB connection with error handling
try:
    mongo_con = MongoIO()
    if hasattr(mongo_con, 'offline_mode') and mongo_con.offline_mode:
        st.warning("⚠️ Running in offline mode. Data will be saved locally but not to MongoDB.")
        st.info("You can still scrape reviews, but they will only be stored locally.")
except Exception as e:
    st.error(f"MongoDB Connection Error: {e}")
    st.info("The application will continue in offline mode with limited functionality.")
    # Create a dummy MongoIO instance for offline mode
    class DummyMongoIO:
        def __init__(self):
            self.offline_mode = True
            
        def store_reviews(self, product_name, reviews):
            # Save to local CSV file as fallback
            try:
                import os
                backup_dir = os.path.join(os.getcwd(), "data_backup")
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, f"{product_name}.csv")
                reviews.to_csv(backup_file, index=False)
                st.success(f"Reviews saved locally to {backup_file}")
                return True
            except Exception as local_e:
                st.error(f"Error saving reviews locally: {local_e}")
                return False
    
    mongo_con = DummyMongoIO()

st.set_page_config(
    "myntra-review-scrapper"

)

st.title("Myntra Review Scrapper")

if "data" not in st.session_state:
    st.session_state["data"] = False





def form_input():
    product = st.text_input("Search Products")
    # Only set the product name in session state if it's not empty
    if product and product.strip():
        st.session_state[SESSION_PRODUCT_KEY] = product
    
    no_of_products = st.number_input("No of products to search",
                                     step=1,
                                     min_value=1)

    if st.button("Scrape Reviews"):
        # Validate product name before proceeding
        if not product or not product.strip():
            st.error("Please enter a product name before scraping reviews.")
            return None
            
        scrapper = ScrapeReviews(
            product_name=product,
            no_of_products=int(no_of_products)
        )

        try:
            # First try to  scrape the data
            scrapped_data = scrapper.get_review_data()
            if scrapped_data is not None and not scrapped_data.empty:
                st.session_state["data"] = True
                
                # Display the scraped data first, so user has access to it even if DB fails
                st.success(f"Successfully scraped {len(scrapped_data)} reviews for '{product}'")
                st.dataframe(scrapped_data)
                
                # Then try to store in MongoDB with separate error handling
                try:
                    mongoio = MongoIO()
                    mongoio.store_reviews(product_name=product, reviews=scrapped_data)
                    st.success("✅ Reviews successfully stored in the database")
                except Exception as db_error:
                    st.warning("⚠️ Reviews were scraped successfully but could not be stored in the database")
                    st.error(f"Database error: {str(db_error)}")
                    st.info("💡 You can still view the scraped data above, but it won't be available for analysis later.\n" +
                           "Please check your internet connection and try again.")
            else:
                st.warning(f"No reviews found for '{product}'. Try another product.")
        except Exception as e:
            st.error(f"Error scraping reviews: {str(e)}")
            import traceback
            st.text(traceback.format_exc())


if __name__ == "__main__":
    data = form_input()
