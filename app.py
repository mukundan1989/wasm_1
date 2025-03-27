import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.title("Stock Open/Close Prices & IndexedDB Storage")

# Function to fetch stock data
def fetch_stock_data(ticker, days=30):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    return data[['Date', 'Open', 'Close']].to_json(orient='records')

# Input for stock symbol
ticker = st.text_input("Enter Stock Symbol (e.g., AAPL):")
days_to_fetch = st.slider("Number of days to fetch:", 1, 365, 30)

if st.button("Fetch & Store Stock Data"):
    if ticker:
        stock_data_json = fetch_stock_data(ticker, days_to_fetch)
        st.success(f"Stock data for {ticker} fetched and stored!")
        
        # JavaScript for IndexedDB storage
        st.components.v1.html(f"""
        <script>
            var db;
            var request = indexedDB.open("StockDatabase", 1);
            request.onupgradeneeded = function(event) {{
                db = event.target.result;
                if (!db.objectStoreNames.contains("stocks")) {{
                    db.createObjectStore("stocks", {{ keyPath: "symbol" }});
                }}
            }};
            request.onsuccess = function(event) {{
                db = event.target.result;
                var transaction = db.transaction(["stocks"], "readwrite");
                var store = transaction.objectStore("stocks");
                store.put({{ symbol: "{ticker}", data: {stock_data_json} }});
            }};
        </script>
        """, height=0)
    else:
        st.warning("Please enter a stock symbol.")

# Retrieve stored data
st.subheader("Retrieve Stored Data")
retrieve_ticker = st.text_input("Enter Stock Symbol to Retrieve:")
if st.button("Retrieve Data"):
    st.components.v1.html(f"""
    <script>
        var db;
        var request = indexedDB.open("StockDatabase", 1);
        request.onsuccess = function(event) {{
            db = event.target.result;
            var transaction = db.transaction(["stocks"], "readonly");
            var store = transaction.objectStore("stocks");
            var getRequest = store.get("{retrieve_ticker}");
            getRequest.onsuccess = function() {{
                if (getRequest.result) {{
                    var stockData = JSON.stringify(getRequest.result.data);
                    var streamlitDataDiv = document.createElement("div");
                    streamlitDataDiv.innerHTML = "<pre>" + stockData + "</pre>";
                    document.body.appendChild(streamlitDataDiv);
                }} else {{
                    alert("No stored data found for this stock symbol.");
                }}
            }};
        }};
    </script>
    """, height=0)

st.info("Stock price data is fetched from Yahoo Finance using yfinance library and stored in IndexedDB.")
