import streamlit as st

st.title("WASM Data Store Test")

st.write("This app uses WebAssembly (via JavaScript) to store and retrieve stock data in IndexedDB.")

# JavaScript function for IndexedDB storage
indexeddb_script = """
<script>
function storeData() {
    let stock = document.getElementById('stockName').value;
    let date = document.getElementById('stockDate').value;
    let openPrice = document.getElementById('openPrice').value;
    let closePrice = document.getElementById('closePrice').value;
    let key = stock + '_' + date;
    let value = JSON.stringify({open: openPrice, close: closePrice});
    
    let request = indexedDB.open("WASM_DB", 1);
    request.onupgradeneeded = function(event) {
        let db = event.target.result;
        if (!db.objectStoreNames.contains("store")) {
            db.createObjectStore("store");
        }
    };
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction("store", "readwrite");
        let store = transaction.objectStore("store");
        store.put(value, key);
        alert("Stock data stored successfully!");
    };
}

function getData() {
    let stock = document.getElementById('retrieveStock').value;
    let date = document.getElementById('retrieveDate').value;
    let key = stock + '_' + date;
    
    let request = indexedDB.open("WASM_DB", 1);
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction("store", "readonly");
        let store = transaction.objectStore("store");
        let dataRequest = store.get(key);
        dataRequest.onsuccess = function() {
            let result = dataRequest.result ? JSON.parse(dataRequest.result) : "No data found";
            document.getElementById('retrievedValue').innerText = result.open ? `Open: ${result.open}, Close: ${result.close}` : result;
        };
    };
}
</script>
"""

# Display JavaScript in Streamlit
st.components.v1.html(f"""
{indexeddb_script}
<input type='text' id='stockName' placeholder='Stock Name'>
<input type='date' id='stockDate'>
<input type='text' id='openPrice' placeholder='Open Price'>
<input type='text' id='closePrice' placeholder='Close Price'>
<button onclick='storeData()'>Store Data</button>
<br><br>
<input type='text' id='retrieveStock' placeholder='Stock Name'>
<input type='date' id='retrieveDate'>
<button onclick='getData()'>Retrieve Data</button>
<p id='retrievedValue'></p>
""", height=350)
