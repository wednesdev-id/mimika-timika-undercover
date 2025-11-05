"""
Kompas.com News Scraper
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
from utils.helpers import clean_text, extract_date, log_site_status

def scrape_kompas():
    """
    Scrape latest news from Kompas.com
    Returns pandas.DataFrame with columns: title, date, url, description, category
    """
    articles = []
    base_url = "https://www.kompas.com"

    try:
        # Get latest news page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Scrape from multiple sections
        sections = [
            'https://www.kompas.com/news',
            'https://www.kompas.com/nasional',
            'https://www.kompas.com/ekonomi',
            'https://www.kompas.com/bola',
            'https://www.kompas.com/tekno',
            'https://www.kompas.com/otomotif'
        ]

        for section_url in sections:
            try:
                logging.info(f"Scraping section: {section_url}")
                response = requests.get(section_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find article links - Kompas uses specific CSS classes
                article_links = soup.find_all('a', class_='article__link')

                for link in article_links[:10]:  # Limit to 10 articles per section
                    try:
                        article_url = link.get('href')
                        if not article_url or not article_url.startswith('http'):
                            continue

                        # Get article details
                        article_response = requests.get(article_url, headers=headers, timeout=10)
                        article_response.raise_for_status()
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')

                        # Extract title
                        title_elem = article_soup.find('h1', class_='read__title')
                        title = clean_text(title_elem.get_text()) if title_elem else ""

                        # Extract date
                        date_elem = article_soup.find('div', class_='read__time')
                        date_text = date_elem.get_text() if date_elem else ""
                        date = extract_date(date_text)

                        # Extract description
                        desc_elem = article_soup.find('div', class_='read__content')
                        description = ""
                        if desc_elem:
                            # Get first paragraph as description
                            first_p = desc_elem.find('p')
                            if first_p:
                                description = clean_text(first_p.get_text())
                                # Limit description length
                                if len(description) > 200:
                                    description = description[:200] + "..."

                        # Extract category from URL path
                        category = article_url.split('/')[3] if len(article_url.split('/')) > 3 else "news"

                        if title and article_url:
                            articles.append({
                                'title': title,
                                'date': date.strftime('%Y-%m-%d %H:%M:%S'),
                                'url': article_url,
                                'description': description,
                                'category': category,
                                'source': 'Kompas.com'
                            })

                        # Random delay to be respectful
                        time.sleep(random.uniform(1, 2))

                    except Exception as e:
                        logging.warning(f"Error scraping article {article_url}: {str(e)}")
                        continue

                # Delay between sections
                time.sleep(random.uniform(2, 3))

            except Exception as e:
                logging.warning(f"Error scraping section {section_url}: {str(e)}")
                continue

        log_site_status("Kompas.com", "OK")

    except Exception as e:
        log_site_status("Kompas.com", "ERROR", str(e))
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(articles)

    # Remove duplicates
    if 'url' in df.columns:
        df = df.drop_duplicates(subset=['url'], keep='first')

    logging.info(f"Successfully scraped {len(df)} articles from Kompas.com")
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = scrape_kompas()
    if not df.empty:
        print(f"Scraped {len(df)} articles:")
        print(df[['title', 'date', 'category']].head())
    else:
        print("No articles scraped")