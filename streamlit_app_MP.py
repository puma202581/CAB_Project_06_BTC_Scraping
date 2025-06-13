# To install Streamlit, run the following command in your terminal:
# pip install streamlit

import streamlit as st

from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import numpy as np
import mplcursors

load_dotenv()

def get_api_data():
    dbconn = os.getenv("DBCONN")
    conn = psycopg2.connect(dbconn)
    df = pd.read_sql("SELECT * FROM stock_data;", conn)
    conn.close()
    return df

api_data_btc = get_api_data()

def get_api_data2():
    dbconn = os.getenv("DBCONN")
    conn = psycopg2.connect(dbconn)
    df = pd.read_sql("SELECT * FROM articles;", conn)
    conn.close()
    return df

api_data_news = get_api_data2()

def get_api_data3():
    dbconn = os.getenv("DBCONN")
    conn = psycopg2.connect(dbconn)
    df = pd.read_sql("SELECT * FROM weekly_sentiment_analysis;", conn)
    conn.close()
    return df

sentiment_results = get_api_data3()

# only this line works to display the dataframe in streamlit
# st.title("Daily Prices Data")
# st.dataframe(api_data, use_container_width=True)


# Display the columns to debug
# st.write("Columns in DataFrame:", api_data_btc.columns.tolist())

with st.container():
    st.header("Stay up-to-date regarding Bitcoin (BTC)")
    st.write(
        "This app was generated to test web scraping and setting up an environment to refresh used data on a regular basis. "
        "Refresh cycle is once a day at 09h00 CET. Feedback is welcome."
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
    filtered_btc = api_data_btc.sort_values('date', ascending=False)

with st.container():
    st.subheader("BTC - Daily Raw Data")
    df_display = filtered_btc[['date', 'open_price', 'close_price', 'volume']].reset_index(drop=True)
    df_display['open_price'] = df_display['open_price'].map('{:.2f}'.format)
    df_display['close_price'] = df_display['close_price'].map('{:.2f}'.format)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

with st.container():
    st.subheader("BTC - High/Low Range & Average by Day (Candlestick Style)")
    import plotly.graph_objects as go

    # Prepare data
    df_candle = filtered_btc.set_index('date')[['low_price', 'high_price']].copy()
    df_candle['average_price'] = (df_candle['low_price'] + df_candle['high_price']) / 2

    # Identify top and bottom 3 average_price values
    top3 = df_candle['average_price'].nlargest(3)
    bottom3 = df_candle['average_price'].nsmallest(3)

    fig = go.Figure()

   

    # Create candlestick chart using Plotly's Candlestick trace
    fig.add_trace(go.Candlestick(
        x=filtered_btc['date'],
        open=filtered_btc['open_price'],
        high=filtered_btc['high_price'],
        low=filtered_btc['low_price'],
        close=filtered_btc['close_price'],
        increasing_line_color='green',
        decreasing_line_color='red',
        name='Candlestick',
        showlegend=True
    ))

    # Calculate moving averages
    ma10 = filtered_btc['close_price'].rolling(window=10).mean()
    ma30 = filtered_btc['close_price'].rolling(window=30).mean()

    # Add 10-day moving average
    fig.add_trace(go.Scatter(
        x=filtered_btc['date'],
        y=ma10,
        mode='lines',
        line=dict(color='blue', width=2),
        name='MA 10',
        hovertemplate='Date: %{x}<br>MA10: %{y:.2f}<extra></extra>'
    ))

    # Add 30-day moving average
    fig.add_trace(go.Scatter(
        x=filtered_btc['date'],
        y=ma30,
        mode='lines',
        line=dict(color='orange', width=2),
        name='MA 30',
        hovertemplate='Date: %{x}<br>MA30: %{y:.2f}<extra></extra>'
    ))

# Note the crossover between the two moving averages, which may be a sign that momentum has shifted from bullish to bearish 
# (or vice versa, as shown in the crossover in the chart)

    # # Add average price line
    # fig.add_trace(go.Scatter(
    #     x=df_candle.index, y=df_candle['average_price'],
    #     mode='lines+markers',
    #     line=dict(color='blue', width=2),
    #     name='Average (High/Low)',
    #     hovertemplate='Date: %{x}<br>Avg: %{y:.2f}<extra></extra>'
    # ))

    # # Add top 3 points
    # fig.add_trace(go.Scatter(
    #     x=top3.index, y=top3.values,
    #     mode='markers',
    #     marker=dict(color='green', size=12),
    #     name='Top 3 Avg',
    #     hovertemplate='Date: %{x}<br>Avg: %{y:.2f}<extra></extra>'
    # ))

    # # Add bottom 3 points
    # fig.add_trace(go.Scatter(
    #     x=bottom3.index, y=bottom3.values,
    #     mode='markers',
    #     marker=dict(color='red', size=12),
    #     name='Bottom 3 Avg',
    #     hovertemplate='Date: %{x}<br>Avg: %{y:.2f}<extra></extra>'
    # ))

    # # Add trend line for average price
    # x = np.arange(len(df_candle))
    # y = df_candle['average_price'].values
    # z = np.polyfit(x, y, 1)
    # p = np.poly1d(z)
    # fig.add_trace(go.Scatter(
    #     x=df_candle.index, y=p(x),
    #     mode='lines',
    #     line=dict(color='red', dash='dash', width=2),
    #     name='Trend',
    #     hoverinfo='skip'
    # ))

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        # title='BTC - High/Low Range & Average by Day (Candlestick Style)',
        # title_x=0.5,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=40, r=40, t=60, b=40),
        xaxis=dict(
            tickmode='array',
            tickvals=df_candle.index[::7],
            ticktext=[pd.to_datetime(d).strftime('%Y-%m-%d') for d in df_candle.index[::7]],
            tickangle=90
        )
    )

    st.plotly_chart(fig, use_container_width=True)

with st.container():
    st.subheader("BTC - Trade Volume by Day")
    import matplotlib.pyplot as plt

    # Prepare data
    volume_data = filtered_btc.set_index('date')['volume']

    # Plot histogram
    fig, ax = plt.subplots()
    ax.bar(volume_data.index, volume_data.values, color='blue', label='Volume')

    # Show every 7th date on x-axis
    formatted_dates = [pd.to_datetime(d).strftime('%Y-%m-%d') for d in volume_data.index]
    ax.set_xticks(volume_data.index[::7])
    ax.set_xticklabels([formatted_dates[i] for i in range(0, len(formatted_dates), 7)], rotation=270)
    ax.grid(True, linestyle='--', alpha=0.5)

    ax.set_xlabel('Date')
    ax.set_ylabel('Volume')
    # ax.set_title('BTC - Trade Volume by Day')
    plt.tight_layout()

    st.pyplot(fig)

with st.container():
    st.subheader("BTC - News articles | Source: U.today.com")
    st.dataframe(api_data_news[['title', 'date', 'author', 'link']], use_container_width=True)


# Display sentiment analysis results
with st.container():
    st.subheader("BTC - Sentiment Distribution (Latest vs Previous Week)")
    st.write(
        "The underlying sentiment analysis is reviewing headers and contents of collected articles every week. "
        "It uses keywords and NLTK VADER lexicon with SentimentIntensityAnalyzer."
    )

    # Ensure 'created_at' is datetime
    sentiment_results['created_at'] = pd.to_datetime(sentiment_results['created_at'])

    # Get the two most recent dates (ignore time)
    sentiment_results['created_date'] = sentiment_results['created_at'].dt.date
    latest_dates = sentiment_results['created_date'].sort_values(ascending=False).unique()[:2]

    if len(latest_dates) < 2:
        st.write("Not enough data to display two pie charts.")
    else:
        # Prepare data for both dates
        pie_data = []
        for d in latest_dates:
            df = sentiment_results[sentiment_results['created_date'] == d]
            counts = df.set_index('sentiment_category')['category_count']
            total_count = counts.sum()
            pie_data.append((d, counts, total_count))

        # Display side-by-side
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{pie_data[0][0]}**")
            st.plotly_chart(
            go.Figure(
                data=[go.Pie(labels=pie_data[0][1].index, values=pie_data[0][1].values, hole=0.3)],
                layout=go.Layout(margin=dict(t=0, b=0, l=0, r=0))
            ),
            use_container_width=True
            )
            st.caption(f"Distribution based on {pie_data[0][2]} articles")
        with col2:
            st.markdown(f"**{pie_data[1][0]}**")
            st.plotly_chart(
            go.Figure(
                data=[go.Pie(labels=pie_data[1][1].index, values=pie_data[1][1].values, hole=0.3)],
                layout=go.Layout(margin=dict(t=0, b=0, l=0, r=0))
            ),
            use_container_width=True
            )
            st.caption(f"Distribution based on {pie_data[1][2]} articles")


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
