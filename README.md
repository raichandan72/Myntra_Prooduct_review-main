# 🛍️ Myntra Review Scraper & Dashboard

A powerful **Python-based** project that scrapes product reviews from Myntra, stores them in **MongoDB** (or local backups), and visualizes insights using a **Streamlit dashboard**.

Get **real-time** reviews, ratings, and pricing info for Myntra products — scraped, structured, and visualized in style.

---

## 📦 Features
- ✅ Scrapes **multiple product listings** and their reviews from Myntra  
- ✅ Extracts **product details**: name, price, rating, reviews, reviewer name & date  
- ✅ Handles **infinite scrolling** to capture all reviews  
- ✅ Stores reviews in **MongoDB** or saves locally as **CSV** if offline  
- ✅ Visualizes key insights using **Streamlit + Plotly**  
- ✅ Robust fallback and **error-handling mechanisms**  

---

## 🛠️ Tech Stack

| Component     | Technology                           |
|--------------|---------------------------------------|
| **Backend**  | Python, Selenium, BeautifulSoup       |
| **Data**     | Pandas, MongoDB                        |
| **Dashboard**| Streamlit, Plotly                      |
| **Cloud**    | MongoDB Atlas                          |

---

## 📂 Project Structure
├── scrape.py # Core web scraper using Selenium + BS4

├── generate_data_report.py # Streamlit dashboard generator

├── init.py # MongoDB I/O operations (MongoIO class)

├── data.csv # Example scraped data

├── data_backup/ # Local CSV backups if MongoDB fails

├── requirements.txt # All dependencies

└── README.md # Project documentation

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/myntra-review-scraper.git
cd myntra-review-scraper

2️⃣ Set Up Environment

Make sure you have Python 3.8+ installed.

Install dependencies:
pip install -r requirements.txt
3️⃣ MongoDB Setup
Create a MongoDB Atlas cluster

Whitelist your IP & get the connection string

Replace it inside __init__.py → mongo_db_url

💡 No MongoDB? No problem!
The script automatically saves data locally in data_backup/ if MongoDB is unreachable.

🚀 Usage
Option 1: Run the Scraper Script
bash
Copy
Edit
python scrape.py
Or use programmatically:

python
Copy
Edit
from scrape import ScrapeReviews

scraper = ScrapeReviews(product_name="Nike Shoes", no_of_products=3)
df = scraper.get_review_data()
print(df.head())
Option 2: Visualize with Streamlit
bash
Copy
Edit
streamlit run generate_data_report.py
📊 Dashboard Insights
The Streamlit dashboard includes:

📈 Average price & rating charts

✅ Best reviews

❌ Worst reviews

📆 Review date trends

🔢 Rating distribution

All interactive and beautiful — thanks to Plotly and Streamlit.

🧠 Offline Mode
If your internet drops or MongoDB is unreachable:

Data is stored in /data_backup/

You can still generate reports from saved CSVs

🧪 Sample Data Format (data.csv)
Product Name	Over_All_Rating	Price	Date	Rating	Name	Comment

📌 To-Do / Future Ideas
 Add CLI tool for interactive product selection

 Deploy dashboard on Streamlit Cloud

 Integrate sentiment analysis on comments

 Schedule scraper with cron job

 Add GUI using Tkinter or a web frontend

📄 License
MIT License — Do what you want, but don’t be evil 😈

👨‍💻 Author
Chandan – LinkedIn
