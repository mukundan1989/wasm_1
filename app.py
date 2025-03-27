import streamlit as st
import yfinance as yf
import datetime

st.title("WASM Data Store Test")

st.write("This app fetches last 1 month price data for AAPL from Yahoo Finance, stores it in IndexedDB, and allows retrieval.")

# Fetch last 1 month data for AAPL
symbol = "AAPL"
end_date = datetime.datetime.today().date()
start_date = end_date - datetime.timedelta(days=30)
data = yf.download(symbol, start=start_date, end=end_date)

# Convert data to JSON format
price_data = data[['Open', 'Close']].to_dict(orient='index')

# JavaScript function for IndexedDB storage
indexeddb_script = f"""
<script>
function storeData() {{
    let priceData = {price_data};
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
        for (let date in priceData) {{
            let value = JSON.stringify(priceData[date]);
            store.put(value, date);
        }}
        alert("Stock data stored successfully!");
    }};
}}

function getData() {{
    let date = document.getElementById('retrieveDate').value;
    let request = indexedDB.open("WASM_DB", 1);
    request.onsuccess = function(event) {{
        let db = event.target.result;
        let transaction = db.transaction("store", "readonly");
        let store = transaction.objectStore("store");
        let dataRequest = store.get(date);
        dataRequest.onsuccess = function() {{
            let result = dataRequest.result ? JSON.parse(dataRequest.result) : "No data found";
            document.getElementById('retrievedValue').innerText = result.Open ? `Open: ${result.Open}, Close: ${result.Close}` : result;
        }};
    }};
}}
</script>
"""

# Display JavaScript in Streamlit
st.components.v1.html(f"""
{indexeddb_script}
<button onclick='storeData()'>Store Last 1 Month Data</button>
<br><br>
<input type='date' id='retrieveDate'>
<button onclick='getData()'>Retrieve Data</button>
<p id='retrievedValue'></p>
""", height=350)
