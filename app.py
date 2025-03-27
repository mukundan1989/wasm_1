import streamlit as st

st.title("WASM Data Store Test")

st.write("This app uses WebAssembly (via JavaScript) to store and retrieve data in IndexedDB.")

# Input fields for data storage
key = st.text_input("Enter Key:")
value = st.text_input("Enter Value:")

# JavaScript function for IndexedDB storage
indexeddb_script = """
<script>
function storeData() {
    let key = document.getElementById('storeKey').value;
    let value = document.getElementById('storeValue').value;
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
        alert("Data stored successfully!");
    };
}

function getData() {
    let key = document.getElementById('retrieveKey').value;
    let request = indexedDB.open("WASM_DB", 1);
    request.onsuccess = function(event) {
        let db = event.target.result;
        let transaction = db.transaction("store", "readonly");
        let store = transaction.objectStore("store");
        let dataRequest = store.get(key);
        dataRequest.onsuccess = function() {
            document.getElementById('retrievedValue').innerText = dataRequest.result || "No data found";
        };
    };
}
</script>
"""

# Display JavaScript in Streamlit
st.components.v1.html(f"""
{indexeddb_script}
<input type='text' id='storeKey' placeholder='Enter Key'>
<input type='text' id='storeValue' placeholder='Enter Value'>
<button onclick='storeData()'>Store Data</button>
<br><br>
<input type='text' id='retrieveKey' placeholder='Enter Key to Retrieve'>
<button onclick='getData()'>Retrieve Data</button>
<p id='retrievedValue'></p>
""", height=300)
