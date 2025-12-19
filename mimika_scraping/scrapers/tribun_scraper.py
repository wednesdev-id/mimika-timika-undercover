"""
Tribunnews.com News Scraper
Scrapes Tribun-papua.com Mimika section for static HTML reliability
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import os
import sys
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
        # Very basic date extraction logic for standalone
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

def scrape_tribun():
    """
    Scrape news from Tribun-papua.com (Mimika section)
    Returns dict with success status and article data
    """
    articles = []
    # Using the static section is much more reliable than JS-rendered search
    base_url = "https://papua.tribunnews.com/mimika"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://papua.tribunnews.com/",
        }
        
        # Check if running on Vercel to avoid timeouts
        is_vercel = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None
        
        logging.info(f"Starting Tribun (Papua) scrape from: {base_url}")
        
        # In Vercel, we only scrape the first page
        max_pages = 1 if is_vercel else 3
        
        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}" if page > 1 else base_url
            
            try:
                logging.info(f"Scraping page {page}")
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Tribun Papua layout:
                # ul class="lpk"
                #   li
                #     div class="pos-rel" (contains img and link)
                #     div 
                #       h3 class="f18 fbo" (title)
                #       h4 class="f14 grey" (description)
                #       div class="grey" (date)
                
                article_items = soup.select('ul.lpk li')
                
                if not article_items:
                    logging.info(f"No more articles found on page {page}")
                    break
                
                found_on_page = 0
                for item in article_items:
                    try:
                        title_elem = item.select_one('h3')
                        if not title_elem:
                            continue
                            
                        link_elem = title_elem.find('a')
                        if not link_elem:
                            continue
                            
                        url = link_elem.get('href')
                        if not url:
                            continue
                            
                        title = clean_text(title_elem.get_text())
                        
                        # Date
                        date_elem = item.find('div', class_='grey') or item.find('time')
                        date_str = clean_text(date_elem.get_text()) if date_elem else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Description
                        desc_elem = item.find('h4')
                        description = clean_text(desc_elem.get_text()) if desc_elem else ""
                        
                        articles.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'date': date_str,
                            'category': 'mimika',
                            'source': 'Tribunnews.com'
                        })
                        found_on_page += 1
                        
                    except Exception as e:
                        continue
                
                if found_on_page == 0:
                    break
                    
                logging.info(f"Found {found_on_page} articles on page {page}")
                
                if page < max_pages:
                    time.sleep(random.uniform(1, 3))
            
            except Exception as e:
                logging.warning(f"Error scraping page {page}: {str(e)}")
                break
        
        log_site_status("Tribunnews.com", "OK")
    
    except Exception as e:
        log_site_status("Tribunnews.com", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Tribun scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    unique_articles = remove_duplicates(articles)
    categories = sorted(list(set(a.get('category', 'mimika') for a in unique_articles)))
    
    return {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': ['Tribunnews.com'],
                'categories': categories
            },
            'articles': unique_articles
        }
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_tribun()
    print(json.dumps(result, indent=2))
