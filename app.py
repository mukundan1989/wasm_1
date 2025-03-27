import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

st.title("Stock Open/Close Prices & Data Store Test")

# Function to fetch stock data
def fetch_stock_data(ticker, days=30):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    return data[['Date', 'Open', 'Close']]

# Input for stock name
ticker = st.text_input("Enter Stock Symbol (e.g., AAPL):")
days_to_fetch = st.slider("Number of days to fetch:", 1, 365, 30)

if st.button("Fetch Stock Data"):
    if ticker:
        stock_data = fetch_stock_data(ticker, days_to_fetch)
        st.dataframe(stock_data, hide_index=True)
        
        # Convert data to JSON format for storage
        stock_json = stock_data.to_json(orient='records')
        
        # Store fetched data in IndexedDB
        st.components.v1.html(f"""
        <script>
        let request = indexedDB.open("WASM_DB", 1);
        request.onupgradeneeded = function(event) {{
            let db = event.target.result;
            if (!db.objectStoreNames.contains("store")) {{
                db.createObjectStore("store");
            }}
        }};
        request.onsuccess = function(event) {{
            let db = event.target.result;
            let transaction = db.transaction("store", "readwrite");
            let store = transaction.objectStore("store");
            store.put({stock_json}, "{ticker}");
            alert("Stock data stored successfully!");
        }};
        </script>
        """, height=0)
    else:
        st.warning("Please enter a stock symbol.")

# IndexedDB JavaScript script for retrieval
indexeddb_script = """
<script>
function getData() {
    let key = document.getElementById('retrieveKey').value;
    let request = indexedDB.open("WASM_DB", 1);
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction("store", "readonly");
        let store = transaction.objectStore("store");
        let dataRequest = store.get(key);
        dataRequest.onsuccess = function() {
            document.getElementById('retrievedValue').innerText = JSON.stringify(dataRequest.result) || "No data found";
        };
    };
}
</script>
"""

# Retrieve UI
st.components.v1.html(f"""
{indexeddb_script}
<input type='text' id='retrieveKey' placeholder='Enter Stock Symbol to Retrieve'>
<button onclick='getData()'>Retrieve Data</button>
<p id='retrievedValue'></p>
""", height=300)

st.info("Stock price data is fetched from Yahoo Finance using yfinance library.")
