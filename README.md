# 🚀 Data Intelligence Dashboard

**Author:** Aarush Kothari  

## 🧭 Overview
This project is a mini financial data platform built to collect, process, and visualize stock market data. It features a robust Python backend serving REST APIs, an interactive frontend dashboard, and an integrated Machine Learning model that forecasts next-day market trends based on technical indicators.

## ⚙️ Tech Stack
* **Backend:** FastAPI, Python, SQLite
* **Data Processing:** Pandas, Pandas-TA, yfinance
* **Machine Learning:** XGBoost Classifier
* **Frontend:** HTML5, Tailwind CSS, Vanilla JS, Chart.js

## ✨ System Logic & Architecture
### 1. Data Pipeline & Storage
* Fetches 1 year of historical daily data for a curated watchlist using `yfinance`.
* Cleans and formats the data into a Pandas DataFrame.
* Calculates core metrics: **Daily Return**, **7-Day Moving Average**, and **52-Week High/Low**.
* **Custom Insight:** Calculates the **Average True Range (ATR)** to serve as a volatility score for each asset.
* Stores processed data in a lightweight local `SQLite` database for rapid API querying.

### 2. REST API (FastAPI)
Exposes the following endpoints with auto-generated Swagger UI documentation (available at `/docs`):
* `GET /companies`: Returns the active stock watchlist.
* `GET /data/{symbol}`: Returns the last 30 days of clean pricing data.
* `GET /summary/{symbol}`: Returns the calculated 52-week highs/lows and average close.
* `GET /predict/{symbol}`: Triggers the XGBoost model to return a Bullish/Bearish prediction.

### 3. AI Prediction Logic
* **Why XGBoost?** Gradient boosting algorithms excel at finding complex, non-linear relationships in tabular financial data compared to standard linear regression.
* **How it works:** After the database is populated, the system trains a unique, lightweight model for each stock in memory. 
* **The Features:** It uses the closing price, intraday momentum (`daily_return`), short-term trend (`ma_7`), and volatility (`atr_14`) to learn historical patterns. 
* **The Target:** It predicts a binary outcome: `1` (Bullish - tomorrow's close will be higher) or `0` (Bearish - tomorrow's close will be lower).

---

## 🖥️ The Interactive Dashboard
The frontend is a single-page application designed for clarity and speed, built with HTML5, Vanilla JavaScript, and Tailwind CSS.
* **Asynchronous Loading:** When a user clicks a stock in the sidebar, the JavaScript makes concurrent `fetch()` calls to the data, summary, and prediction APIs.
* **Visualization:** It utilizes **Chart.js** to render a clean, interactive line graph of the 30-day closing prices, allowing users to hover over data points for exact daily valuations.

---

## 🛠️ Setup & Run Instructions

**1. Clone the repository**
```bash
git clone [https://github.com/aarushkothari/stock-intelligence-dashboard.git](https://github.com/aarushkothari/stock-intelligence-dashboard.git)
cd stock-intelligence-dashboard
```
**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r req.txt
```
**3. Run the Backend Server**
```bash
uvicorn app:app --reload
```
**4. View the Dashboard**
```
Open the index.html file in any modern web browser to interact with the visualizations.
```

**5. View the API Documentation**
With the server running, navigate to http://127.0.0.1:8000/docs in your browser to interact with the auto-generated Swagger UI and test the endpoints directly.
