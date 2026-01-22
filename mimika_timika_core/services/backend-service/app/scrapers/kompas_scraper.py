"""
Kompas.com News Scraper
Scrapes Kompas search results for "mimika timika" keyword
"""

import requests
from bs4 import BeautifulSoup
import time
import random
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

def scrape_kompas(keyword="mimika timika"):
    """
    Scrape news from Kompas.com search with keyword
    Returns dict with success status and article data
    """
    articles = []
    # keyword param used directly
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Referer": "https://www.kompas.com/",
            "Connection": "keep-alive",
        }
        
        # Check if running on Vercel to avoid timeouts
        is_vercel = os.environ.get('VERCEL') == '1' or os.environ.get('VERCEL_ENV') is not None
        
        # Get custom limit from env or use defaults (Kompas default logic logic handled in loop)
        custom_limit = os.environ.get('SCRAPE_PAGES_LIMIT')
        actual_max_pages = 2 # Default for Vercel
        
        if custom_limit:
            try:
                actual_max_pages = int(custom_limit)
                logging.info(f"[Kompas.com] Using custom page limit: {actual_max_pages}")
            except ValueError:
                logging.warning(f"[Kompas.com] Invalid SCRAPE_PAGES_LIMIT")
        
        if is_vercel:
            logging.info(f"Vercel detected - limiting scrape to {actual_max_pages} pages to avoid 10s timeout")

        logging.info(f"[Kompas.com] Starting search for keyword: '{keyword}'")
        
        page = 1
        while True:
            # Check for page limit if on Vercel
            if is_vercel and page > actual_max_pages:
                logging.info("[Kompas.com] Vercel page limit reached. Stopping scrape.")
                break

            search_url = f"https://search.kompas.com/search?q={keyword.replace(' ', '+')}&page={page}&sort=latest&site_id=all"
            
            try:
                logging.info(f"[Kompas.com] Scraping page {page}")
                response = requests.get(search_url, headers=headers, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Based on user's screenshot, the structure is:
                # div class="articleList -list "
                #   div class="articleItem"
                #     a class="article-link"
                #       div class="articleItem-box"
                #         h2 class="articleTitle"
                #       div class="articlePost"
                #         div class="articlePost-date"
                #       div class="articleLead"
                #         p (description)

                article_list_container = soup.find('div', class_='articleList')
                if not article_list_container:
                    # Alternative selector if the first one fails
                    article_list_container = soup.find('section', class_='sectionBox')
                
                if not article_list_container:
                    logging.info(f"[Kompas.com] No article list container found on page {page}")
                    break
                    
                article_items = article_list_container.find_all('div', class_='articleItem')
                
                if not article_items:
                    # Try direct article find if div.articleItem is not used identically everywhere
                    article_items = article_list_container.find_all('article', class_='articleList')

                if not article_items:
                    logging.info(f"[Kompas.com] No more articles found on page {page}")
                    break
                
                found_on_page = 0
                for item in article_items:
                    try:
                        # Find the link first to get the URL
                        link_elem = item.find('a', class_='article-link') or item.find('a')
                        if not link_elem:
                            continue
                            
                        url = link_elem.get('href')
                        if not url:
                            continue
                            
                        # Title
                        title_elem = item.find('h2', class_='articleTitle') or item.find('h2')
                        if not title_elem:
                            continue
                        title = clean_text(title_elem.get_text())
                        
                        # Date
                        date_elem = item.find('div', class_='articlePost-date')
                        date_str = clean_text(date_elem.get_text()) if date_elem else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Description
                        desc_elem = item.find('div', class_='articleLead')
                        description = ""
                        if desc_elem:
                            p_elem = desc_elem.find('p')
                            description = clean_text(p_elem.get_text()) if p_elem else clean_text(desc_elem.get_text())
                        
                        # Categorization
                        # Use helper with Title/URL fallback
                        # Kompas URL usually contains category like /nasional/, /regional/, etc.
                        # We pass the raw segment from URL if possible, or just "news" and let helper decide
                        raw_category = "news"
                        if len(url.split('/')) > 3:
                             raw_category = url.split('/')[3] # e.g. kompas.com/[read]/... NO, kompas.com/[regional]/...
                        
                        from ..utils.helpers import normalize_category
                        category = normalize_category(raw_category, title, url)

                        # Image Extraction
                        # Structure: div.articleItem -> a.article-link -> div.articleItem-wrap -> div.articleItem-img -> img
                        image_url = ""
                        wrap_div = item.find('div', class_='articleItem-wrap')
                        if wrap_div:
                            img_div = wrap_div.find('div', class_='articleItem-img')
                            if img_div:
                                img_elem = img_div.find('img')
                                if img_elem:
                                    image_url = img_elem.get('src') or img_elem.get('data-src', '')
                                    # Fallback for lazy loading
                                    if 'placeholder' in image_url or not image_url:
                                        image_url = img_elem.get('data-src', '')
                        
                        # Fallback if structure changes
                        if not image_url:
                            img_elem = item.find('img')
                            if img_elem:
                                image_url = img_elem.get('src') or img_elem.get('data-src', '')
                        
                        articles.append({
                            'title': title,
                            'url': url,
                            'description': description,
                            'date': date_str,
                            'category': category,
                            'category': category,
                            'source': 'Kompas.com',
                            'image_url': image_url
                        })
                        found_on_page += 1
                        
                    except Exception as e:
                        logging.debug(f"Error parsing item: {str(e)}")
                        continue
                
                if found_on_page == 0:
                    break
                    
                logging.info(f"[Kompas.com] Found {found_on_page} articles on page {page}")
                
                # Delay
                time.sleep(random.uniform(0.5, 1.5) if is_vercel else random.uniform(2, 4))
                page += 1
                
                # Safety break for non-Vercel
                if not is_vercel and page > 50:
                    break
            
            except Exception as e:
                logging.warning(f"[Kompas.com] Error scraping page {page}: {str(e)}")
                break
        
        log_site_status("Kompas.com", "OK")
    
    except Exception as e:
        log_site_status("Kompas.com", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Kompas scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # Final cleanup
    unique_articles = remove_duplicates(articles)
    categories = sorted(list(set(a.get('category', 'news') for a in unique_articles)))
    
    return {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': ['Kompas.com'],
                'categories': categories
            },
            'articles': unique_articles
        }
    }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_kompas()
    print(json.dumps(result, indent=2))