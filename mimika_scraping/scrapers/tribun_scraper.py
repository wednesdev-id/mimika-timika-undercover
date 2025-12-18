"""
Tribunnews.com News Scraper
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from datetime import datetime
from utils.helpers import clean_text, extract_date, log_site_status

def scrape_tribun():
    """
    Scrape latest news from Tribunnews.com
    Returns dict with response format consistent with API endpoints:
    {
        'status': 'success' | 'error',
        'data': {
            'metadata': {...},
            'articles': [...]
        } | 'message': 'error message'
    }
    """
    articles = []
    base_url = "https://www.tribunnews.com"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Scrape from multiple sections
        sections = [
            'https://www.tribunnews.com/nasional',
            'https://www.tribunnews.com/regional',
            'https://www.tribunnews.com/ekonomi',
            'https://www.tribunnews.com/techno',
            'https://www.tribunnews.com/sport',
            'https://www.tribunnews.com/entertainment'
        ]

        for section_url in sections:
            try:
                logging.info(f"Scraping section: {section_url}")
                response = requests.get(section_url, headers=headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find article links - Tribun uses various CSS classes
                article_links = []

                # Try different selectors for article links
                selectors = [
                    'a.title',
                    'a[href*="/"]',
                    'h3 a',
                    'h4 a',
                    '.pt15 a'
                ]

                for selector in selectors:
                    links = soup.select(selector)
                    article_links.extend(links)

                # Filter and deduplicate links
                seen_urls = set()
                filtered_links = []
                for link in article_links:
                    href = link.get('href', '')
                    if href and href not in seen_urls:
                        # Only include article URLs
                        if '/202' in href or '/berita' in href or '/news' in href:
                            seen_urls.add(href)
                            filtered_links.append(link)

                for link in filtered_links[:10]:  # Limit to 10 articles per section
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
                        title_selectors = [
                            'h1',
                            '.f50',
                            '.title',
                            'h2'
                        ]

                        title = ""
                        for selector in title_selectors:
                            title_elem = article_soup.select_one(selector)
                            if title_elem:
                                title = clean_text(title_elem.get_text())
                                if title and len(title) > 10:  # Ensure it's a meaningful title
                                    break

                        # Extract date - try multiple selectors
                        date_selectors = [
                            'time',
                            '.time',
                            '.date',
                            '.published'
                        ]

                        date_text = ""
                        for selector in date_selectors:
                            date_elem = article_soup.select_one(selector)
                            if date_elem:
                                date_text = date_elem.get_text() or date_elem.get('datetime', '')
                                if date_text:
                                    break

                        date = extract_date(date_text)

                        # Extract description
                        description = ""

                        # Try to find description in multiple ways
                        desc_selectors = [
                            '.baca',
                            '.desc',
                            '.summary',
                            'meta[name="description"]'
                        ]

                        for selector in desc_selectors:
                            desc_elem = article_soup.select_one(selector)
                            if desc_elem:
                                if desc_elem.name == 'meta':
                                    description = clean_text(desc_elem.get('content', ''))
                                else:
                                    description = clean_text(desc_elem.get_text())
                                if description:
                                    break

                        # If no description found, get first paragraph
                        if not description:
                            content_selectors = [
                                '.side-article',
                                '.content',
                                'div p'
                            ]

                            for selector in content_selectors:
                                content_elem = article_soup.select_one(selector)
                                if content_elem:
                                    first_p = content_elem.find('p')
                                    if first_p:
                                        description = clean_text(first_p.get_text())
                                        if len(description) > 200:
                                            description = description[:200] + "..."
                                        break

                        # Extract category from URL path
                        path_parts = article_url.split('/')
                        category = "news"
                        if len(path_parts) > 3:
                            potential_category = path_parts[3]
                            if potential_category in ['nasional', 'regional', 'ekonomi', 'techno', 'sport', 'entertainment']:
                                category = potential_category

                        if title and article_url and len(title) > 15:  # Ensure title is meaningful
                            articles.append({
                                'title': title,
                                'date': date.strftime('%Y-%m-%d %H:%M:%S'),
                                'url': article_url,
                                'description': description,
                                'category': category,
                                'source': 'Tribunnews.com'
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

        log_site_status("Tribunnews.com", "OK")

    except Exception as e:
        log_site_status("Tribunnews.com", "ERROR", str(e))
        return {
            'status': 'error',
            'message': f'Tribun scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

    # Remove duplicates
    seen_urls = set()
    unique_articles = []
    for article in articles:
        if article.get('url') not in seen_urls:
            seen_urls.add(article.get('url'))
            unique_articles.append(article)

    # Prepare response data
    if not unique_articles:
        return {
            'status': 'success',
            'data': {
                'metadata': {
                    'total_articles': 0,
                    'last_updated': datetime.now().isoformat(),
                    'sources': ['Tribunnews.com'],
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
                'sources': ['Tribunnews.com'],
                'categories': sorted(categories)
            },
            'articles': unique_articles
        }
    }

    logging.info(f"Successfully scraped {len(unique_articles)} articles from Tribunnews.com")
    return response_data

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = scrape_tribun()
    if result['status'] == 'success':
        articles = result['data']['articles']
        print(f"Scraped {len(articles)} articles:")
        for article in articles[:5]:  # Show first 5 articles
            print(f"- {article.get('title', 'N/A')} ({article.get('category', 'N/A')})")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")