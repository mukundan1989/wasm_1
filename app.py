import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Set page title
st.set_page_config(page_title="AAPL Stock Prices")

# Title for the app
st.title("AAPL Open/Close Prices")

# Function to fetch stock data
def fetch_stock_data(days=30):
    # Calculate date range
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    
    # Fetch data from Yahoo Finance
    ticker = "AAPL"
    data = yf.download(ticker, start=start_date, end=end_date)
    
    # Reset index to make Date a column
    data = data.reset_index()
    
    # Convert Date to string for display
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    
    return data[['Date', 'Open', 'Close']]  # Return only needed columns

# Sidebar for user input
st.sidebar.header("Settings")
days_to_fetch = st.sidebar.slider("Number of days to fetch:", 1, 365, 30)

# Fetch and display data
st.subheader(f"AAPL Open/Close Prices (Last {days_to_fetch} days)")
data = fetch_stock_data(days_to_fetch)

# Display the data table
st.dataframe(data, hide_index=True)

# Add some info
st.info("Data fetched from Yahoo Finance using yfinance library.")
