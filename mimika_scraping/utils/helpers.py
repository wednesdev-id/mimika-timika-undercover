"""
Helper functions for news scraping - Optimized for JSON-only responses
"""

import re
import logging
import json
from datetime import datetime
from typing import List, Dict, Any
import os

def setup_logging():
    """Setup logging configuration"""
    handlers = [logging.StreamHandler()]
    
    # Try to add file handler, but don't fail if filesystem is read-only (e.g., Vercel)
    try:
        os.makedirs('logs', exist_ok=True)
        handlers.append(logging.FileHandler('logs/scrape_log.txt'))
    except (OSError, PermissionError):
        # Serverless environments like Vercel have read-only filesystems
        # Just use console logging
        pass
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters"""
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    return text

def extract_date(date_text: str) -> datetime:
    """Extract and standardize date from text"""
    if not date_text:
        return datetime.now()

    # Common Indonesian date formats
    date_patterns = [
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
        r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
    ]

    for pattern in date_patterns:
        match = re.search(pattern, date_text)
        if match:
            try:
                if pattern == date_patterns[0] or pattern == date_patterns[1]:
                    day, month, year = map(int, match.groups())
                else:
                    year, month, day = map(int, match.groups())
                return datetime(year, month, day)
            except ValueError:
                continue

    return datetime.now()

def remove_duplicates(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate articles based on URL"""
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    return unique_articles

def log_site_status(site_name: str, status: str, error_msg: str = None):
    """Log scraping status for each site"""
    if status == "OK":
        logging.info(f"[{site_name}] Scraping completed successfully")
    else:
        logging.error(f"[{site_name}] Scraping failed: {error_msg}")

def validate_article(article: Dict[str, Any]) -> bool:
    """Validate if article has required fields"""
    required_fields = ['title', 'url']

    for field in required_fields:
        if not article.get(field):
            return False

    return True