# To install Streamlit, run the following command in your terminal:
# pip install streamlit

import streamlit as st
import psycopg2
import pandas as pd

# Set the page configuration


def get_api_data():
    dbconn = st.secrets["DBCONN"]
    conn = psycopg2.connect(dbconn)
    df = pd.read_sql("SELECT * FROM daily_prices;", conn)
    conn.close()
    return df

api_data_btc = get_api_data()

def get_api_data2():
    dbconn = st.secrets["DBCONN"]
    conn = psycopg2.connect(dbconn)
    df = pd.read_sql("SELECT * FROM news;", conn)
    conn.close()
    return df

api_data_news = get_api_data2()

# only this line works to display the dataframe in streamlit
# st.title("Daily Prices Data")
# st.dataframe(api_data, use_container_width=True)


# Display the columns to debug
# st.write("Columns in DataFrame:", api_data_btc.columns.tolist())

with st.container():
    st.header("Stay up-to-date regarding Bitcoin (BTC)")
    st.write(
        "This app was generated to test web scraping and setting up an environment to refresh used data on a regular basis. "
        "Refresh cycle is once a day at XXhXX CET. Feedback is welcome."
    )

# Adjust column names as needed (example: lowercase or actual names from your DB)
# Add a selection box for filtering
filter_option = st.selectbox(
    "Select date range for BTC data:",
    ('All', 'Last 10 Days', 'Last 30 Days')
)

# Prefilter api_data_btc based on selection
if filter_option == 'Last 10 Days':
    filtered_btc = api_data_btc.sort_values('date', ascending=False).head(10).sort_values('date', ascending=False)
elif filter_option == 'Last 30 Days':
    filtered_btc = api_data_btc.sort_values('date', ascending=False).head(30).sort_values('date', ascending=False)
else:
    filtered_btc = api_data_btc

with st.container():
    st.subheader("BTC - Daily Raw Data")
    st.dataframe(filtered_btc[['date', 'open', 'close', 'volume']], use_container_width=True)

with st.container():
    st.subheader("BTC - Closing Value by day")
    st.line_chart(filtered_btc.set_index('date')['close'])
    
with st.container():
    st.subheader("BTC - Trade Volume by day")
    st.line_chart(filtered_btc.set_index('date')['volume'])

with st.container():
    st.subheader("BTC - News articles | Source: U.today.com")
    st.dataframe(api_data_news[['title', 'date', 'author', 'link']], use_container_width=True)

# st.title("Daily Prices Line Chart")

# # Ensure 'Date' column is datetime
# api_data['Date'] = pd.to_datetime(api_data['Date'])

# # Drop columns not needed for the chart, keep only 'Date', 'Open', 'Close'
# api_data = api_data[['Date', 'Open', 'Close']]

# # Date selection widgets
# min_date = api_data['Date'].min().date()
# max_date = api_data['Date'].max().date()

# start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
# end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)

# # Filter data based on selected dates
# filtered_data = api_data[(api_data['Date'] >= pd.to_datetime(start_date)) & (api_data['Date'] <= pd.to_datetime(end_date))]

# # Create a line chart for 'Open' and 'Close' prices over time
# st.line_chart(filtered_data.set_index('Date')[['Open', 'Close']])
