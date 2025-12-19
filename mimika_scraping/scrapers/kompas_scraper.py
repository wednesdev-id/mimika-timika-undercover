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

# Add parent directory to path for imports when running standalone  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.helpers import clean_text, extract_date, log_site_status
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

def scrape_kompas():
    """
    Scrape news from Kompas.com search with keyword "mimika timika"
    
    Returns:
        dict: Response format:
        {
            'status': 'success' | 'error',
            'data': {
                'metadata': {
                    'total_articles': int,
                    'last_updated': ISO timestamp,
                    'sources': ['Kompas.com'],
                    'categories': list
                },
                'articles': list of dicts
            }
        }
    """
    articles = []
    keyword = "mimika timika"
    # No page limit - scrape until no more articles found
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.kompas.com/",
            "Connection": "keep-alive",
        }
        
        logging.info(f"Starting search for keyword: '{keyword}' - scraping ALL pages until no more results")
        
        # Kompas search URL with keyword - Continue until no more articles
        page = 1
        while True:
            search_url = f"https://search.kompas.com/search?q={keyword.replace(' ', '+')}&page={page}&sort=latest&site_id=all&last_date=all"
            
            try:
                logging.info(f"Scraping page {page}")
                response = requests.get(search_url, headers=headers, timeout=15)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find article list container - based on screenshot HTML structure
                # The container is <div class="articleList -list">
                article_list = soup.find('div', class_='articleList')
                
                if not article_list:
                    logging.warning(f"No article list found on page {page}")
                    break
                
                # Find all article items
                article_items = article_list.find_all('div', class_='articleItem')
                
                if not article_items:
                    logging.warning(f"No articles found on page {page}")
                    break
                
                logging.info(f"Found {len(article_items)} articles on page {page}")
                
                for item in article_items:
                    try:
                        # Extract article link - <a class="article-link" href="...">
                        link_elem = item.find('a', class_='article-link')
                        if not link_elem:
                            continue
                        
                        url = link_elem.get('href', '')
                        if not url:
                            continue
                        
                        # Extract title - <h2 class="articleTitle">
                        title_elem = item.find('h2', class_='articleTitle')
                        if not title_elem:
                            continue
                        title = clean_text(title_elem.get_text())
                        
                        # Extract description - <div class="articleLead"><p>
                        desc_elem = item.find('div', class_='articleLead')
                        description = ""
                        if desc_elem:
                            p_elem = desc_elem.find('p')
                            if p_elem:
                                description = clean_text(p_elem.get_text())
                        
                        # Extract date - <div class="articlePost-date">
                        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        datetime_obj = datetime.now()
                        
                        date_elem = item.find('div', class_='articlePost-date')
                        if date_elem:
                            date_text = clean_text(date_elem.get_text())
                            # Parse date like "13 December 2025"
                            try:
                                # Try to parse the date
                                from dateutil import parser
                                parsed_date = parser.parse(date_text)
                                date_str = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                                datetime_obj = parsed_date
                            except:
                                # If parsing fails, use current time
                                pass
                        
                        # Extract category from URL
                        category = "news"
                        if url:
                            url_parts = url.split('/')
                            if len(url_parts) > 3:
                                potential_category = url_parts[3]
                                # Kompas categories
                                if potential_category in ['aktivitas', 'global', 'nasional', 'megapolitan', 'ekonomi', 'tekno', 'otomotif', 'bola', 'entertainment', 'properti', 'travel', 'lifestyle', 'kolom']:
                                    category = potential_category
                        
                        if title and url:
                            data = {
                                "title": title,
                                "url": url,
                                "description": description,
                                "date": date_str,
                                "category": category,
                                "source": "Kompas.com",
                                "datetime_obj": datetime_obj
                            }
                            articles.append(data)
                    
                    except Exception as e:
                        logging.warning(f"Error parsing article: {str(e)}")
                        continue
                
                # Random delay between pages
                time.sleep(random.uniform(2, 4))
                
                # Increment page counter
                page += 1
            
            except Exception as e:
                logging.warning(f"Error scraping page {page}: {str(e)}")
                # On error, try next page
                page += 1
                continue
        
        # Sort by datetime (newest first)
        articles.sort(key=lambda x: x.get("datetime_obj", datetime.now()), reverse=True)
        
        # Remove datetime_obj from final data
        for item in articles:
            if "datetime_obj" in item:
                del item["datetime_obj"]
        
        log_site_status("Kompas.com", "OK")
        logging.info(f"Successfully scraped {len(articles)} articles with keyword '{keyword}'")
    
    except Exception as e:
        log_site_status("Kompas.com", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Kompas scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }
    
    # Remove duplicates
    seen_urls = set()
    unique_articles = []
    for article in articles:
        if article.get('url') not in seen_urls:
            seen_urls.add(article.get('url'))
            unique_articles.append(article)
    
    # Prepare response
    if not unique_articles:
        return {
            'status': 'success',
            'data': {
                'metadata': {
                    'total_articles': 0,
                    'last_updated': datetime.now().isoformat(),
                    'sources': ['Kompas.com'],
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
                'sources': ['Kompas.com'],
                'categories': sorted(categories)
            },
            'articles': unique_articles
        }
    }
    
    return response_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_kompas()
    if result['status'] == 'success':
        articles = result['data']['articles']
        print(f"\nScraped {len(articles)} articles from Kompas.com:")
        for article in articles[:10]:  # Show first 10 articles
            print(f"\n- {article.get('title', 'N/A')}")
            print(f"  Category: {article.get('category', 'N/A')}")
            print(f"  URL: {article.get('url', 'N/A')[:80]}...")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
