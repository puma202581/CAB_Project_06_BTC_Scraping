# import pandas as pd
import requests
from bs4 import BeautifulSoup


def scrape_bitcoin_news():
    url = "https://u.today/search/node?keys=bitcoin"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract article titles, dates, authors, and links
    main_block = soup.find('main', class_='main-block')
    articles = main_block.find_all('div', class_='news__item') if main_block else []
    data = []
    seen = set()
    for article in articles:
        # Title
        title_tag = article.find('div', class_='news__item-title')
        title = title_tag.get_text(strip=True) if title_tag else 'No Title'
        # Date
        date_tag = article.find('div', class_='humble')
        date = date_tag.get_text(strip=True) if date_tag else 'No Date'
        # Author
        author_tag = article.find('a', class_='humble humble--author')
        author = author_tag.get_text(strip=True) if author_tag else 'Unknown'
        # Link
        link_tag = article.find('a', class_='news__item-body')
        link = link_tag['href'] if link_tag and link_tag.has_attr('href') else 'No Link'

        # Use (title, date, author, link) as a unique identifier
        identifier = (title, date, author, link)
        if identifier not in seen:
            data.append({
                'Title': title,
                'Date': date,
                'Author': author,
                'Link': link
            })
            seen.add(identifier)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data)
    print(data)
    return df
    
# Testing the function
# Uncomment the following lines to test the function directly
if __name__ == "__main__":
    try:
        data = scrape_bitcoin_news()
        print("Fetched data:")
        # print(data)
    except Exception as e:
        print(f"An error occurred: {e}")