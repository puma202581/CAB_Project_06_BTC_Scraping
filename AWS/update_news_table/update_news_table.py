import os
import psycopg2
from datetime import datetime as dt

def insert_articles(event, context):
    data = event.get("data", [])
    dbconn = os.getenv("DBCONN")
    conn = psycopg2.connect(dbconn)
    cursor = conn.cursor()
    for article in data:
        # Convert 'Date' string to datetime object
        # Example format: "Jun 10, 2025 - 11:52"
        try:
            date = dt.strptime(article['Date'], "%b %d, %Y - %H:%M")
        except ValueError:
            # Fallback: try without time if time is missing
            date = dt.strptime(article['Date'], "%b %d, %Y")
        # Store as a datetime object; PostgreSQL 'timestamp' or 'timestamptz' columns natively support Python datetime objects
        cursor.execute('''
            INSERT INTO articles (Title, Date, Author, Link)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (Title, Date) DO NOTHING
        ''', (article['Title'], date, article['Author'], article['Link']))
    conn.commit()
    cursor.close()
    conn.close()
# For local testing only:
if __name__ == "__main__":
    event = {
        "data": [
            {"Title": "Is Bitcoin Safe From Quantum Computers? Michael Saylor Shares Bullish Take", "Date": "Jun 09, 2025 - 11:52", "Author": "Yuri Molchan", "Link": "https://u.today/is-bitcoin-safe-from-quantum-computers-michael-saylor-shares-bullish-take"},
            {"Title": "Dogecoin Cofounder Breaks Silence on Bitcoin Price Surge: Details", "Date": "Jun 10, 2025 - 10:49", "Author": "Tomiwabold Olajide", "Link": "https://u.today/dogecoin-cofounder-breaks-silence-on-bitcoin-price-surge-details"}
        ]
    }
    print(lambda_handler(event, None))

# data = [{"Title": "Is Bitcoin Safe From Quantum Computers? Michael Saylor Shares Bullish Take", "Date": "Jun 09, 2025 - 11:52", "Author": "Yuri Molchan", "Link": "https://u.today/is-bitcoin-safe-from-quantum-computers-michael-saylor-shares-bullish-take"}, {"Title": "Dogecoin Cofounder Breaks Silence on Bitcoin Price Surge: Details", "Date": "Jun 10, 2025 - 10:49", "Author": "Tomiwabold Olajide", "Link": "https://u.today/dogecoin-cofounder-breaks-silence-on-bitcoin-price-surge-details"}]
# insert_all_articles_from_data(data)
