🛍️ Myntra Review Scraper & Dashboard
A powerful Python-based project that scrapes product reviews from Myntra, stores them in MongoDB (or local backups), and visualizes insights using a Streamlit dashboard.

🔍 Get real-time reviews, ratings, and pricing info for Myntra products — scraped, structured, and visualized in style.

📦 Features
✅ Scrapes multiple product listings and their reviews from Myntra
✅ Extracts product details: name, price, rating, reviews, reviewer name & date
✅ Handles infinite scrolling to capture all reviews
✅ Stores reviews in MongoDB or saves locally as CSV if offline
✅ Visualizes key insights using Streamlit + Plotly
✅ Robust fallback and error-handling mechanisms
🛠️ Tech Stack
Component	Technology
Backend	Python, Selenium, BeautifulSoup
Data Handling	Pandas, MongoDB
Dashboard	Streamlit, Plotly
Cloud Storage	MongoDB Atlas
├── scrape.py # Core web scraper using Selenium + BS4

├── generate_data_report.py # Streamlit dashboard generator

├── init.py # MongoDB I/O operations (MongoIO class)

├── data.csv # Scraped data output (example)

├── data_backup/ # Local CSV backups if MongoDB fails

├── requirements.txt # All dependencies

└── README.md # You're reading it!

⚙️ Installation & Setup
1. Clone the Repo
git clone https://github.com/your-username/myntra-review-scraper.git
cd myntra-review-scraper

2. Set Up Environment
Make sure you have Python 3.8+ installed.

Install dependencies:


pip install -r requirements.txt

3. MongoDB Setup
Create a MongoDB Atlas cluster

Whitelist your IP & get the connection string

Replace it inside __init__.py in mongo_db_url

Don’t want cloud storage? No worries — it automatically saves data locally if MongoDB is unreachable.


🚀 How to Use
Option 1: Run Scraper Script

python scrape.py
Or import and use programmatically:


from scrape import ScrapeReviews

scraper = ScrapeReviews(product_name="Nike Shoes", no_of_products=3)
df = scraper.get_review_data()
print(df.head())

Option 2: Visualize with Streamlit

streamlit run generate_data_report.py

📊 Sample Insights
The dashboard includes:

📈 Average price & rating charts

✅ Best reviews

❌ Worst reviews

📆 Review dates

🔢 Rating distribution

All interactive and beautiful thanks to Plotly and Streamlit.

🧠 Bonus: Offline Mode
If your network drops or MongoDB is unreachable:

All data is stored in /data_backup/

You can still generate reports using those CSVs

🧪 Sample Output
data.csv


├── Product Name
├── Over_All_Rating
├── Price
├── Date
├── Rating
├── Name
└── Comment
📌 To-Do / Ideas
 Add CLI tool to interactively pick products

 Deploy dashboard on Streamlit Cloud

 Add sentiment analysis to comments

 Schedule scraper with cron job

 Add GUI with tkinter or web frontend

📄 License
MIT License. Do what you want, but don’t be evil 😈

👨‍💻 Author
Chandan – LinkedIn