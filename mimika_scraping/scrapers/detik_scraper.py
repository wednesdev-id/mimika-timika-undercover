"""
Detik.com News Scraper
"""

from django import urls
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
from utils.helpers import clean_text, extract_date, log_site_status

def scrape_detik():
    """
    Scrape latest news from Detik.com with search keyword "mimika timika"
    Returns pandas.DataFrame with columns: title, date, url, description, category
    """
    articles = []
    base_url = "https://www.detik.com"
    keyword = "mimika timika"
    max_pages = 100

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        logging.info(f"Starting search for keyword: '{keyword}'")

        # Collect HTML from all pages
        html_pages = []
        for page in range(1, max_pages + 1):
            search_url = f"https://www.detik.com/search/searchall?query={keyword.replace(' ', '%20')}&page={page}&result_type=latest"

            try:
                logging.info(f"Scraping page {page}")
                response = requests.get(search_url, headers=headers, timeout=10)
                response.raise_for_status()
                html_pages.append(response.text)
                time.sleep(random.uniform(2, 4))
            except Exception as e:
                logging.warning(f"Error scraping page {page}: {str(e)}")
                continue

        # Parse all HTML content
        berita = []
        for html_content in html_pages:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Use the same structure as test_scrape.py
            main = soup.find('div', class_="container-fluid")
            if not main:
                continue

            articles = main.find('div', class_="column-6")
            if not articles:
                continue

            article = articles.find_all('div', class_="list-content")
            if not article:
                continue

            for links in article:
                links = links.find_all('article', class_="list-content__item")
                for link in links:
                    try:
                        # Extract title
                        title_elem = link.find('h3', class_="media__title")
                        if not title_elem:
                            continue
                        title = clean_text(title_elem.text.strip())

                        # Extract href
                        link_elem = link.find('a')
                        href = link_elem['href'] if link_elem else ""

                        # Extract description
                        desc_elem = link.find('div', class_="media__desc")
                        description = clean_text(desc_elem.text.strip()) if desc_elem else ""

                        # Extract timestamp
                        date_elem = link.find('div', class_="media__date")
                        if date_elem and date_elem.find('span') and date_elem.find('span').get('d-time'):
                            try:
                                time_timestamp = int(date_elem.find('span')['d-time'])
                                from datetime import datetime
                                from zoneinfo import ZoneInfo
                                time_datetime = datetime.fromtimestamp(time_timestamp, tz=ZoneInfo("Asia/Jakarta"))
                                date_str = time_datetime.strftime('%Y-%m-%d %H:%M:%S')
                                datetime_obj = time_datetime
                            except:
                                date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                datetime_obj = datetime.now()
                        else:
                            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            datetime_obj = datetime.now()

                        # Set default category (removed complex logic)
                        category = "news"

                        data = {
                            "title": title,
                            "url": href,
                            "description": description,
                            "date": date_str,
                            "category": category,
                            "source": "Detik.com",
                            "datetime_obj": datetime_obj
                        }
                        berita.append(data)

                    except Exception as e:
                        logging.warning(f"Error parsing article: {str(e)}")
                        continue

        # Sort by datetime (newest first)
        berita.sort(key=lambda x: x["datetime_obj"], reverse=True)

        # Remove datetime_obj from final data
        for item in berita:
            del item["datetime_obj"]

        articles = berita
        log_site_status("Detik.com", "OK")
        logging.info(f"Successfully scraped {len(articles)} articles with keyword '{keyword}'")

    except Exception as e:
        log_site_status("Detik.com", "ERROR", str(e))
        return pd.DataFrame()

    # Convert to DataFrame and remove duplicates
    df = pd.DataFrame(articles)
    if 'url' in df.columns:
        df = df.drop_duplicates(subset=['url'], keep='first')

    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = scrape_detik()
    if not df.empty:
        print(f"Scraped {len(df)} articles:")
        print(df[['title', 'date', 'category']].head())
    else:
        print("No articles scraped")