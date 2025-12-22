"""
Kumparan.com News Scraper
Simplified scraper for Kumparan.com news
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
import sys
import os
from datetime import datetime
import re
import json

# Add parent directory to path for imports when running standalone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.helpers import clean_text, extract_date, log_site_status, remove_duplicates
except ImportError:
    # Fallback implementations for standalone testing
    def clean_text(text):
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text.strip())
        text = re.sub(r'<[^>]+>', '', text)
        return text

    def extract_date(date_text):
        return datetime.now()

    def log_site_status(site, status, error=None):
        if status == "OK":
            logging.info(f"[{site}] Scraping completed successfully")
        else:
            logging.error(f"[{site}] Scraping failed: {error}")

    def remove_duplicates(articles):
        seen = set()
        unique = []
        for a in articles:
            if a['url'] not in seen:
                seen.add(a['url'])
                unique.append(a)
        return unique

def scrape_kumparan():
    """
    Simplified Kumparan scraper
    Returns dict with success status and minimal article data
    """
    articles = []

    try:
        # Simple headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://kumparan.com/",
            "Connection": "keep-alive",
        }

        # Try to get latest news from Kumparan
        urls_to_try = [
            "https://kumparan.com/",
            "https://kumparan.com/kumparannews",
            "https://kumparan.com/search/mimika"
        ]

        articles_found = 0
        max_articles = 5  # Limit to prevent timeout

        for url in urls_to_try:
            if articles_found >= max_articles:
                break

            try:
                logging.info(f"Trying Kumparan URL: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # Look for article links
                article_links = soup.find_all('a', href=True)

                for link in article_links:
                    if articles_found >= max_articles:
                        break

                    href = link.get('href', '')

                    # Check if it's a Kumparan article
                    if ('kumparan.com' in href or href.startswith('/')) and len(href) > 10:
                        # Skip certain URLs
                        if any(skip in href.lower() for skip in ['login', 'register', 'search', 'tag', '#']):
                            continue

                        # Make URL absolute
                        if href.startswith('/'):
                            href = f"https://kumparan.com{href}"
                        elif not href.startswith('http'):
                            continue

                        # Get title from link or nearby elements
                        title = ""
                        title_elem = link.find('h1') or link.find('h2') or link.find('h3') or link.find('h4')
                        if title_elem:
                            title = clean_text(title_elem.get_text())
                        else:
                            title = clean_text(link.get_text())

                        # Skip if title is too short or empty
                        if len(title) < 10:
                            continue

                        # Try to get description from nearby elements
                        description = ""
                        parent = link.parent
                        if parent:
                            desc_elem = parent.find('p') or parent.find('div', class_=re.compile(r'desc|summary|excerpt'))
                            if desc_elem:
                                description = clean_text(desc_elem.get_text())

                        # Basic category detection from URL
                        category = "news"
                        if '/politik/' in href:
                            category = "politik"
                        elif '/bisnis/' in href or '/ekonomi/' in href:
                            category = "ekonomi"
                        elif '/olahraga/' in href:
                            category = "olahraga"
                        elif '/hiburan/' in href:
                            category = "hiburan"

                        articles.append({
                            'title': title,
                            'url': href,
                            'description': description,
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'category': category,
                            'source': 'Kumparan'
                        })

                        articles_found += 1
                        logging.info(f"Found article: {title[:50]}...")

                # Small delay between URLs
                time.sleep(1)

            except Exception as e:
                logging.warning(f"Error scraping {url}: {str(e)}")
                continue

        log_site_status("Kumparan", "OK")
        logging.info(f"Successfully collected {len(articles)} articles from Kumparan")

    except Exception as e:
        log_site_status("Kumparan", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Kumparan scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

    # Remove duplicates
    unique_articles = remove_duplicates(articles)
    categories = sorted(list(set(a.get('category', 'news') for a in unique_articles)))

    return {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': ['Kumparan'],
                'categories': categories,
                'note': 'Simplified scraper - limited results'
            },
            'articles': unique_articles
        }
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_kumparan()
    print(json.dumps(result, indent=2))
