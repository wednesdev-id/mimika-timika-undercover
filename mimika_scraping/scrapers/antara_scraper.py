"""
Antara News Agency Scraper
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
from utils.helpers import clean_text, extract_date, log_site_status

def scrape_antara():
    """
    Scrape latest news from Antara News
    Returns pandas.DataFrame with columns: title, date, url, description, category
    """
    articles = []
    base_url = "https://www.antaranews.com"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Scrape from multiple sections
        sections = [
            'https://www.antaranews.com/berita',
            'https://www.antaranews.com/politik',
            'https://www.antaranews.com/ekonomi',
            'https://www.antaranews.com/teknologi',
            'https://www.antaranews.com/olahraga',
            'https://www.antaranews.com/hiburan'
        ]

        for section_url in sections:
            try:
                logging.info(f"Scraping section: {section_url}")
                response = requests.get(section_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find article links - Antara uses specific CSS classes
                article_links = soup.find_all('a', class_='article-title')

                for link in article_links[:10]:  # Limit to 10 articles per section
                    try:
                        article_url = link.get('href')
                        if not article_url:
                            continue

                        # Make sure URL is absolute
                        if article_url.startswith('/'):
                            article_url = base_url + article_url

                        # Get article details
                        article_response = requests.get(article_url, headers=headers, timeout=10)
                        article_response.raise_for_status()
                        article_soup = BeautifulSoup(article_response.content, 'html.parser')

                        # Extract title
                        title_elem = article_soup.find('h1', class_='post-title')
                        title = clean_text(title_elem.get_text()) if title_elem else ""

                        # Alternative title selector
                        if not title:
                            title_elem = article_soup.find('h1')
                            title = clean_text(title_elem.get_text()) if title_elem else ""

                        # Extract date
                        date_elem = article_soup.find('div', class_='post-date')
                        date_text = date_elem.get_text() if date_elem else ""
                        date = extract_date(date_text)

                        # Extract description
                        desc_elem = article_soup.find('div', class_='post-content')
                        description = ""
                        if desc_elem:
                            # Get first paragraph as description
                            first_p = desc_elem.find('p')
                            if first_p:
                                description = clean_text(first_p.get_text())
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
                                'source': 'Antara News'
                            })

                        # Random delay
                        time.sleep(random.uniform(1, 2))

                    except Exception as e:
                        logging.warning(f"Error scraping article {article_url}: {str(e)}")
                        continue

                # Delay between sections
                time.sleep(random.uniform(2, 3))

            except Exception as e:
                logging.warning(f"Error scraping section {section_url}: {str(e)}")
                continue

        log_site_status("Antara News", "OK")

    except Exception as e:
        log_site_status("Antara News", "ERROR", str(e))
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(articles)

    # Remove duplicates
    if 'url' in df.columns:
        df = df.drop_duplicates(subset=['url'], keep='first')

    logging.info(f"Successfully scraped {len(df)} articles from Antara News")
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = scrape_antara()
    if not df.empty:
        print(f"Scraped {len(df)} articles:")
        print(df[['title', 'date', 'category']].head())
    else:
        print("No articles scraped")