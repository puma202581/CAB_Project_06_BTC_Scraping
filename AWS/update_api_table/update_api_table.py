import os
import psycopg # might have to use psycopg2 or psycopg3 depending on your setup


# Insert the data into the PostgreSQL database
def insert_data_pg(date, open_price, high_price, low_price, close_price, volume):
    dbconn = os.getenv("DBCONN")
    conn = psycopg.connect(dbconn)  # might have to use psycopg2 or psycopg3 depending on your setup
    cur = conn.cursor()
    try:
        # Check if the date already exists in the database
        cur.execute(
            "SELECT 1 FROM stock_data WHERE date = %s;",
            (date,)
        )
        exists = cur.fetchone()
        if not exists:
            # Insert only if the date does not exist
            cur.execute(
                """
                INSERT INTO stock_data (date, open_price, high_price, low_price, close_price, volume)
                VALUES (%s, %s, %s, %s, %s, %s);
                """,
                (date, open_price, high_price, low_price, close_price, volume)
            )
            conn.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cur.close()
        conn.close()



def insert_time_series(time_series):
    for date, prices in time_series.items():
        insert_data_pg(
            date,
            float(prices["1. open"]),
            float(prices["2. high"]),
            float(prices["3. low"]),
            float(prices["4. close"]),
            int(prices["5. volume"])
        )
        
# Testing the function
# Uncomment the following lines to test the function directly
# if __name__ == "__main__":
#     try:
#         data = get_api_data()
#         print("Fetched time_series data:")
#         print(data)
#         insert_time_series(data)
#     except Exception as e:
#         print(f"An error occurred: {e}")
# This script fetches daily stock data for IBM from the Alpha Vantage API
# and inserts it into a PostgreSQL database, ensuring no duplicate dates are inserted.
# The database connection string is expected to be stored in the environment variable
# DBCONN, and the API key for Alpha Vantage is expected in APLHAVANTAGEAPIKEY.
# The table `stock_data` should have the following schema:
# CREATE TABLE stock_data (
#     date DATE PRIMARY KEY,
#     open_price FLOAT,
#     high_price FLOAT,
#     low_price FLOAT,
#     close_price FLOAT,
#     volume BIGINT
# );
# Ensure that the PostgreSQL database is set up with the correct schema before running this script.
# The script uses the psycopg library to connect to the PostgreSQL database.
