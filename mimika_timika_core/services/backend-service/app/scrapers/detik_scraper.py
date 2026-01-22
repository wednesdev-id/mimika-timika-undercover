"""
Detik.com News Scraper
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import os
import sys
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python versions
    from backports.zoneinfo import ZoneInfo

# Add parent directory to path for imports when running standalone  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ..utils.helpers import clean_text, extract_date, log_site_status, remove_duplicates
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

import re

def scrape_detik(keyword="mimika timika"):
    """
    Scrape latest news from Detik.com with search keyword
    Returns dict with response format consistent with API endpoints
    """
    articles = []
    # keyword param used directly

    max_pages = 100

    try:
        # Check if running on Vercel to avoid timeouts
        is_vercel = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None
        
        # Get custom limit from env or use defaults
        custom_limit = os.environ.get('SCRAPE_PAGES_LIMIT')
        if custom_limit:
            try:
                actual_max_pages = int(custom_limit)
                logging.info(f"[Detik.com] Using custom page limit: {actual_max_pages}")
            except ValueError:
                actual_max_pages = 2 if is_vercel else 5
                logging.warning(f"[Detik.com] Invalid SCRAPE_PAGES_LIMIT, using default: {actual_max_pages}")
        else:
            actual_max_pages = 2 if is_vercel else 5  # Always limit to prevent timeout

        if is_vercel:
            logging.info(f"[Detik.com] Vercel detected - limiting scrape to {actual_max_pages} pages to avoid timeout")
        else:
            logging.info(f"[Detik.com] Local environment - limiting scrape to {actual_max_pages} pages to prevent timeout")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        logging.info(f"[Detik.com] Starting search for keyword: '{keyword}'")

        # Collect HTML from all pages
        html_pages = []
        for page in range(1, actual_max_pages + 1):
            search_url = f"https://www.detik.com/search/searchall?query={keyword.replace(' ', '%20')}&page={page}&sort=time"

            try:
                logging.info(f"[Detik.com] Scraping page {page}")
                response = requests.get(search_url, headers=headers, timeout=10)
                response.raise_for_status()
                html_pages.append(response.text)
                
                # Shorter delay on Vercel to beat the clock
                time.sleep(random.uniform(0.5, 1.5) if is_vercel else random.uniform(2, 4))
            except Exception as e:
                logging.warning(f"[Detik.com] Error scraping page {page}: {str(e)}")
                continue

        # Parse all HTML content
        berita = []
        for html_content in html_pages:
            soup = BeautifulSoup(html_content, 'html.parser')

            main = soup.find('div', class_="container-fluid")
            if not main:
                continue

            articles_container = main.find('div', class_="column-6")
            if not articles_container:
                continue

            article_list = articles_container.find_all('div', class_="list-content")
            if not article_list:
                continue

            for links in article_list:
                article_items = links.find_all('article', class_="list-content__item")
                for link in article_items:
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
                                time_datetime = datetime.fromtimestamp(time_timestamp, tz=ZoneInfo("Asia/Jakarta"))
                                date_str = time_datetime.strftime('%Y-%m-%d %H:%M:%S')
                                datetime_obj = time_datetime
                            except Exception:
                                date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                datetime_obj = datetime.now()
                        else:
                            date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            datetime_obj = datetime.now()

                        # Categorization
                        # Use helper with Title/URL fallback
                        from ..utils.helpers import normalize_category
                        category = normalize_category("news", title, href)
                        
                        # Image Extraction (User requested: class media__image -> img)
                        # Image Extraction
                        # User Rule: class media__image -> img
                        image_url = ""
                        img_div = link.find('div', class_="media__image")
                        if img_div:
                            # Try finding img directly
                            img_elem = img_div.find('img')
                            if img_elem:
                                image_url = img_elem.get('data-src') or img_elem.get('src', '')
                                
                            # Detail uses ratiobox often
                            if not image_url:
                                span_elem = img_div.find('span', class_="ratiobox")
                                if span_elem:
                                     img_elem = span_elem.find('img')
                                     if img_elem:
                                         image_url = img_elem.get('data-src') or img_elem.get('src', '')
                        
                        # Fallback: Find any image in the article element if still empty
                        if not image_url:
                            img_any = link.find('img')
                            if img_any:
                                image_url = img_any.get('data-src') or img_any.get('src', '')

                        data = {
                            "title": title,
                            "url": href,
                            "description": description,
                            "date": date_str,
                            "category": category,
                            "source": "Detik.com",
                            "image_url": image_url,
                            "datetime_obj": datetime_obj
                        }
                        berita.append(data)

                    except Exception as e:
                        logging.warning(f"[Detik.com] Error parsing article: {str(e)}")
                        continue

        # Sort by datetime (newest first)
        berita.sort(key=lambda x: x["datetime_obj"], reverse=True)

        # Remove datetime_obj from final data
        for item in berita:
            del item["datetime_obj"]

        articles = berita
        log_site_status("Detik.com", "OK")
        logging.info(f"[Detik.com] Successfully scraped {len(articles)} articles with keyword '{keyword}'")

    except Exception as e:
        log_site_status("Detik.com", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Detik scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

    # Remove duplicates
    unique_articles = remove_duplicates(articles)
    
    # Prepare response data
    if not unique_articles:
        return {
            'status': 'success',
            'data': {
                'metadata': {
                    'total_articles': 0,
                    'last_updated': datetime.now().isoformat(),
                    'sources': ['Detik.com'],
                    'categories': []
                },
                'articles': []
            }
        }

    categories = list(set(article.get('category', 'news') for article in unique_articles))

    response_data = {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': ['Detik.com'],
                'categories': sorted(categories)
            },
            'articles': unique_articles
        }
    }

    return response_data

if __name__ == "__main__":
    import json
    logging.basicConfig(level=logging.INFO)
    result = scrape_detik()
    print(json.dumps(result, indent=2))
