"""
Narasi.tv News Scraper
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
from utils.helpers import clean_text, extract_date, log_site_status

def scrape_narasi():
    """
    Scrape latest news from Narasi.tv
    Returns pandas.DataFrame with columns: title, date, url, description, category
    """
    articles = []
    base_url = "https://www.narasi.tv"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Scrape from multiple sections
        sections = [
            'https://www.narasi.tv/pages/news',
            'https://www.narasi.tv/pages/politik',
            'https://www.narasi.tv/pages/ekonomi',
            'https://www.narasi.tv/pages/teknologi',
            'https://www.narasi.tv/pages/entertainment'
        ]

        for section_url in sections:
            try:
                logging.info(f"Scraping section: {section_url}")
                response = requests.get(section_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find article links - Narasi uses various CSS classes
                article_links = soup.find_all('a', href=True)

                # Filter links that look like articles
                article_links = [link for link in article_links if
                                link.get('href') and
                                ('/news/' in link.get('href') or '/story/' in link.get('href'))]

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

                        # Extract title - try multiple selectors
                        title_elem = (article_soup.find('h1') or
                                    article_soup.find('h2') or
                                    article_soup.find('title'))

                        title = clean_text(title_elem.get_text()) if title_elem else ""

                        # Extract date - try multiple selectors
                        date_elem = (article_soup.find('time') or
                                    article_soup.find('div', class_='date') or
                                    article_soup.find('span', class_='date'))

                        date_text = date_elem.get_text() if date_elem else ""
                        date = extract_date(date_text)

                        # Extract description
                        description = ""

                        # Try to find description in multiple ways
                        desc_selectors = [
                            'div.description',
                            'div.excerpt',
                            'div.summary',
                            'meta[name="description"]'
                        ]

                        for selector in desc_selectors:
                            desc_elem = article_soup.select_one(selector)
                            if desc_elem:
                                if desc_elem.name == 'meta':
                                    description = clean_text(desc_elem.get('content', ''))
                                else:
                                    description = clean_text(desc_elem.get_text())
                                break

                        # If no description found, get first paragraph
                        if not description:
                            content_elem = article_soup.find('div', class_='content')
                            if content_elem:
                                first_p = content_elem.find('p')
                                if first_p:
                                    description = clean_text(first_p.get_text())
                                    if len(description) > 200:
                                        description = description[:200] + "..."

                        # Extract category from URL path
                        path_parts = article_url.split('/')
                        category = "news"
                        if len(path_parts) > 3:
                            potential_category = path_parts[3]
                            if potential_category in ['news', 'politik', 'ekonomi', 'teknologi', 'entertainment']:
                                category = potential_category

                        if title and article_url:
                            articles.append({
                                'title': title,
                                'date': date.strftime('%Y-%m-%d %H:%M:%S'),
                                'url': article_url,
                                'description': description,
                                'category': category,
                                'source': 'Narasi.tv'
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

        log_site_status("Narasi.tv", "OK")

    except Exception as e:
        log_site_status("Narasi.tv", "ERROR", str(e))
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(articles)

    # Remove duplicates
    if 'url' in df.columns:
        df = df.drop_duplicates(subset=['url'], keep='first')

    logging.info(f"Successfully scraped {len(df)} articles from Narasi.tv")
    return df

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    df = scrape_narasi()
    if not df.empty:
        print(f"Scraped {len(df)} articles:")
        print(df[['title', 'date', 'category']].head())
    else:
        print("No articles scraped")