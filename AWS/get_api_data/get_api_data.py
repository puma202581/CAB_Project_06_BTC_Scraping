import os
import requests

# This script fetches daily stock data for IBM from the Alpha Vantage API

# Insert the data into the database
def get_api_data():
      
    # Fetch the data from the API
    api_key = os.getenv("APLHAVANTAGEAPIKEY")
    endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=" + api_key
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        response_json = response.json()
        time_series = response_json.get("Time Series (Daily)", {})
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
    
    return time_series

# Testing the function
# Uncomment the following lines to test the function directly
# if __name__ == "__main__":
#     try:
#         data = get_api_data()
#         print("Fetched time_series data:")
#         print(data)
#     except Exception as e:
#         print(f"An error occurred: {e}")

