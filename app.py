import sqlite3
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from xgboost import XGBClassifier

app=FastAPI(
    title="Stock Data Intelligence API",
    description="Backend API for querying.",
    version="1.0.0"
)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WATCHLIST = ["RELIANCE.NS","TCS.NS","HDFCBANK.NS","INFY.NS","COALINDIA.NS","INDHOTEL.NS","ADANIENT.NS","UNITDSPR.NS","ITC.NS","IOC.NS","SOLARINDS.NS","TITAN.NS"]

#DATABASE
def db():
    con=sqlite3.connect("stocks.db")
    c=con.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock_data(
        symbol TEXT,
        date TEXT,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume INTEGER,
        daily_return REAL,
        ma_7 REAL,
        atr_14 REAL,
        UNIQUE(symbol,date)
        )
    ''')
    con.commit()
    con.close()

#PIPELINE
def fns_data():
    print("Fetching and processing latest stock data")
    con=sqlite3.connect("stocks.db")

    for symbol in WATCHLIST:
        st=yf.Ticker(symbol)
        df=st.history(period="1y")
        if df.empty:
            continue

        df.reset_index(inplace=True)
        df['Date']=pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
        df['Daily_Return']=(df['Close']-df['Open'])/df['Open']
        df.ta.sma(length=7, append=True)
        df.ta.atr(length=14, append=True)
        df.rename(columns={'SMA_7':'MA_7','ATRr_14':'ATR_14'},inplace=True)
        df.fillna(0,inplace=True)

        for _,row in df.iterrows():
            try:
                con.execute('''
                    INSERT OR REPLACE INTO stock_data(symbol,date,open,high,low,close,volume,daily_return,ma_7,atr_14) VALUES(?,?,?,?,?,?,?,?,?,?)
                ''',(
                    symbol, row['Date'], row['Open'], row['High'], row['Low'], 
                    row['Close'], row['Volume'], row['Daily_Return'], row['MA_7'], row['ATR_14']
                ))
            except sqlite3.Error:
                pass
    con.commit()
    con.close()
    print("DATABASE updated")

models={}
def train_model():
    print("Training AI prediction models...")
    con = sqlite3.connect("stocks.db")
    
    for symbol in WATCHLIST:
        df = pd.read_sql_query(f"SELECT * FROM stock_data WHERE symbol = '{symbol}' ORDER BY date ASC", con)
        
        if len(df) < 50:
            continue
            
        df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)
        df.dropna(inplace=True)
        
        features = ['close', 'daily_return', 'ma_7', 'atr_14']
        X = df[features]
        y = df['Target']
        
        model = XGBClassifier(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42, eval_metric='logloss')
        model.fit(X, y)
        
        models[symbol] = model
        
    con.close()
    print("AI Models trained successfully!")

db()
fns_data()
train_model()


#BACKEND API
@app.get("/companies")
def get_companies():
    return{"companies":WATCHLIST}

@app.get("/data/{symbol}")
def get_data(symbol:str):
    con=sqlite3.connect("stocks.db")
    con.row_factory=sqlite3.Row
    c=con.cursor()

    c.execute("SELECT * FROM stock_data WHERE symbol=? ORDER BY date DESC LIMIT 30",(symbol,))
    rows=c.fetchall()
    con.close()

    if not rows:
        raise HTTPException(status_code=404,detail="Symbol not found or no data available")
    return{"symbol":symbol,"data":[dict(row) for row in rows]}

@app.get("/summary/{symbol}")
def get_summary(symbol:str):
    con=sqlite3.connect("stocks.db")
    c=con.cursor()

    c.execute("SELECT MAX(high), MIN(low), AVG(close) FROM stock_data WHERE symbol = ?", (symbol,))
    row=c.fetchone()
    con.close()

    if not row or row[0] is None:
        raise HTTPException(status_code=404,detail="Symbol not found")
    return{
        "symbol": symbol,
        "52_week_high": round(row[0], 2),
        "52_week_low": round(row[1], 2),
        "average_close": round(row[2], 2)
    }

@app.get("/predict/{symbol}")
def get_prediction(symbol:str):
    if symbol not in models:
        raise HTTPException(status_code=404, detail="AI Model not available for this symbol")
        
    con = sqlite3.connect("stocks.db")
    df = pd.read_sql_query(f"SELECT close, daily_return, ma_7, atr_14 FROM stock_data WHERE symbol = '{symbol}' ORDER BY date DESC LIMIT 1", con)
    con.close()
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Not enough data to predict")
        
    prediction = models[symbol].predict(df)[0]
    
    trend = "BULLISH" if prediction == 1 else "BEARISH"
    color_code = "green" if prediction == 1 else "red"
    
    return {
        "symbol": symbol, 
        "prediction": trend,
        "color": color_code
    }
