"""
SeputarPapua News Scraper
Scrapes news from seputarpapua.com
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
        # Basic fallback
        try:
             # Try to parse specific format if known, else return now
             # Example: "Selasa, 21 Januari 2026 10:00"
             return datetime.now()
        except:
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

def get_article_details(url):
    """
    Fetch article details to get the date and potentially better image/content
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }
        
        # Add delay
        time.sleep(1)
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find date
        # Common selectors for SeputarPapua based on typical structure (inspector needs validation if available)
        # Based on user description, it appears on detail page.
        # Possible candidates: .date, .post-date, time, meta properties
        
        date_obj = datetime.now()
        date_found = False
        
        # Strategy 1: Look for date metadata (often most reliable)
        meta_date = soup.find('meta', property='article:published_time')
        if meta_date:
            try:
                # ISO format usually: 2024-01-21T10:00:00+07:00
                date_str = meta_date.get('content')
                # Parse ISO
                if date_str:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    date_found = True
            except:
                pass
                
        # Strategy 2: Look for visible date element
        if not date_found:
            # Common class names in WP/News themes
            date_selectors = [
                 'div.date', 'span.date', 'div.post-date', 'span.post-date', 
                 'div.entry-date', 'span.entry-date', 'time', '.article-date'
            ]
            
            for selector in date_selectors:
                elem = soup.select_one(selector)
                if elem:
                    try:
                        extracted = extract_date(clean_text(elem.get_text()))
                        if extracted:
                            date_obj = extracted
                            date_found = True
                            break
                    except:
                        continue
        
        return {
            'date': date_obj.strftime('%Y-%m-%d %H:%M:%S'),
            'date_obj': date_obj
        }

    except Exception as e:
        logging.warning(f"Error fetching details for {url}: {e}")
        return None

def scrape_seputarpapua(keyword="mimika"):
    """
    Scrape SeputarPapua.com
    User specified URLs:
    - https://seputarpapua.com/?s=mimika&post_type=post
    - https://seputarpapua.com/?s=timika&post_type=post
    """
    articles = []
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        
        # Construct URL
        base_url = "https://seputarpapua.com/"
        search_url = f"{base_url}?s={keyword}&post_type=post"
        
        logging.info(f"[SeputarPapua] Scraping: {search_url}")
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Target container: div.widget-content
        # Each item: div.article-item
        
        content_div = soup.find('div', class_='widget-content')
        if not content_div:
            # Try finding main container first if structure is nested
            # main-container -> main-wrapper -> main-content -> widget-content
            # Just search for article-item directly as they are unique enough
            items = soup.find_all('div', class_='article-item')
        else:
            items = content_div.find_all('div', class_='article-item')
            
        logging.info(f"[SeputarPapua] Found {len(items)} items")
        
        count = 0
        max_items = 5 # Limit to avoid timeout/rate limit
        
        for item in items:
            if count >= max_items:
                break
                
            try:
                # 1. Title & URL
                text_div = item.find('div', class_='article-text')
                if not text_div:
                    continue
                    
                h3 = text_div.find('h3')
                if not h3:
                    continue
                    
                link = h3.find('a')
                if not link:
                    continue
                    
                title = clean_text(link.get_text())
                url = link.get('href', '')
                
                # Deduplication check in loop (optional but good)
                if any(a['url'] == url for a in articles):
                    continue
                
                # 2. Image
                image_url = ""
                img_div = item.find('div', class_='article-image')
                if img_div:
                    img_tag = img_div.find('img')
                    if img_tag:
                        image_url = img_tag.get('src') or img_tag.get('data-src', '')
                
                # 3. Description
                description = ""
                snippet_div = text_div.find('div', class_='snippet')
                if snippet_div:
                    description = clean_text(snippet_div.get_text())
                
                # 4. Date (Fetch Details)
                # User Requirement: Date is not in list, must click.
                logging.info(f"[SeputarPapua] Fetching details for date: {url}")
                details = get_article_details(url)
                
                date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if details and details.get('date'):
                    date_str = details['date']
                
                # 5. Category
                # Can we deduce category from URL or classes? 
                # e.g. https://seputarpapua.com/view/category/title...
                # Usually URLs might have category. URL structure in screenshot: /view/title-slug.html 
                # (No category in URL). We'll rely on text analysis or generic.
                category = "News"
                
                articles.append({
                    'title': title,
                    'url': url,
                    'description': description,
                    'date': date_str,
                    'category': category,
                    'source': 'SeputarPapua',
                    'image_url': image_url
                })
                
                count += 1
                
            except Exception as e:
                logging.warning(f"[SeputarPapua] Error parsing item: {e}")
                continue
                
        log_site_status("SeputarPapua", "OK")
        
        return {
            'status': 'success',
            'data': {
                'metadata': {
                    'total_articles': len(articles),
                    'source': 'SeputarPapua'
                },
                'articles': articles
            }
        }
        
    except Exception as e:
        log_site_status("SeputarPapua", "ERROR", str(e))
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Test
    print(json.dumps(scrape_seputarpapua(), indent=2))
