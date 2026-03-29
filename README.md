# 🚀 Data Intelligence Dashboard

**Author:** Aarush Kothari  

## 🧭 Overview
This project is a mini financial data platform built to collect, process, and visualize stock market data. It features a robust Python backend serving REST APIs, an interactive frontend dashboard, and an integrated Machine Learning model that forecasts next-day market trends based on technical indicators.

## ⚙️ Tech Stack
* **Backend:** FastAPI, Python, SQLite
* **Data Processing:** Pandas, Pandas-TA, yfinance
* **Machine Learning:** XGBoost Classifier
* **Frontend:** HTML5, Tailwind CSS, Vanilla JS, Chart.js

## ✨ Logic & Architecture
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
* Features an embedded `XGBClassifier` trained dynamically on database initialization.
* Uses short-term momentum (`ma_7`), volatility (`atr_14`), and immediate price action (`daily_return`) as features to predict whether the next trading day's closing price will be higher or lower.

## 🛠️ Setup Instructions

**1. Clone the repository**
```bash
git clone [https://github.com/aarushkothari/stock-intelligence-dashboard.git](https://github.com/aarushkothari/stock-intelligence-dashboard.git)
cd stock-intelligence-dashboard

**2. Create a virtual environment and install dependencies**

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

**3. Run the Backend Server**

uvicorn app:app --reload

**4. View the Dashboard**

Open the index.html file in any modern web browser to interact with the visualizations.