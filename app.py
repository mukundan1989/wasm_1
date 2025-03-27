import streamlit as st
import js2py

st.title("WASM Data Store Test")

st.write("This app uses WebAssembly (via JavaScript) to store and retrieve data in IndexedDB.")

# Input fields for data storage
key = st.text_input("Enter Key:")
value = st.text_input("Enter Value:")

# JavaScript function for IndexedDB storage
js_code = """
function storeData(key, value) {
    return new Promise((resolve, reject) => {
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
            transaction.oncomplete = function() {
                resolve("Data stored successfully!");
            };
        };
        request.onerror = function() {
            reject("Error storing data.");
        };
    });
}
"""

# Button to store data
if st.button("Store Data"):
    js2py.eval_js(js_code)
    js2py.eval_js("storeData('{}', '{}')".format(key, value))
    st.success("Data stored successfully!")

# JavaScript function to retrieve data
retrieve_js_code = """
function getData(key) {
    return new Promise((resolve, reject) => {
        let request = indexedDB.open("WASM_DB", 1);
        request.onsuccess = function(event) {
            let db = event.target.result;
            let transaction = db.transaction("store", "readonly");
            let store = transaction.objectStore("store");
            let dataRequest = store.get(key);
            dataRequest.onsuccess = function() {
                resolve(dataRequest.result || "No data found");
            };
            dataRequest.onerror = function() {
                reject("Error retrieving data.");
            };
        };
        request.onerror = function() {
            reject("Error opening database.");
        };
    });
}
"""

# Input for retrieval
retrieve_key = st.text_input("Enter Key to Retrieve:")

# Button to retrieve data
if st.button("Retrieve Data"):
    js2py.eval_js(retrieve_js_code)
    data = js2py.eval_js("getData('{}')".format(retrieve_key))
    st.write(f"Retrieved Value: {data}")

st.write("Data is stored in your browser's IndexedDB using WebAssembly.")
