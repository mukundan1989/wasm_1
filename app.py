import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Set page title and icon
st.set_page_config(page_title="AAPL Stock Price", page_icon="📈")

# Title for the app
st.title("AAPL Stock Price Fetcher")

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
    
    return data

# Sidebar for user input
st.sidebar.header("Settings")
days_to_fetch = st.sidebar.slider("Number of days to fetch:", 1, 365, 30)

# Fetch and display data
st.subheader(f"AAPL Open/Close Prices (Last {days_to_fetch} days)")
data = fetch_stock_data(days_to_fetch)

# Display the data table
st.dataframe(data[['Date', 'Open', 'Close']], hide_index=True)

# Display a line chart - FIXED VERSION
st.subheader("Price Trend")
if not data.empty:
    try:
        # Ensure we're working with numeric values
        chart_data = data[['Date', 'Open', 'Close']].copy()
        chart_data['Open'] = pd.to_numeric(chart_data['Open'])
        chart_data['Close'] = pd.to_numeric(chart_data['Close'])
        
        # Set Date as index and plot
        st.line_chart(chart_data.set_index('Date'))
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
else:
    st.warning("No data available to display chart.")

# Display latest price
if not data.empty:
    latest = data.iloc[-1]
    st.subheader("Latest Price")
    col1, col2 = st.columns(2)
    col1.metric("Open Price", f"${latest['Open']:.2f}")
    col2.metric("Close Price", f"${latest['Close']:.2f}")

# Add some info
st.info("Data fetched from Yahoo Finance using yfinance library.")
