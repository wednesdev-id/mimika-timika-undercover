"""
Main News Scraper Application - Refactored for JSON-only responses
"""

import argparse
import logging
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import scrapers
# Import scrapers
from ..scrapers.kompas_scraper import scrape_kompas
from ..scrapers.cnn_scraper import scrape_cnn
from ..scrapers.antara_scraper import scrape_antara
from ..scrapers.tempo_scraper import scrape_tempo
from ..scrapers.kumparan_scraper import scrape_kumparan
from ..scrapers.detik_scraper import scrape_detik
from ..scrapers.seputarpapua_scraper import scrape_seputarpapua

from ..utils.helpers import setup_logging, remove_duplicates

# Configuration
SCRAPERS = {
    'detik': scrape_detik,
    'kompas': scrape_kompas,
    'cnn': scrape_cnn,
    'antara': scrape_antara,
    'tempo': scrape_tempo,
    'kumparan': scrape_kumparan,
    'seputarpapua': scrape_seputarpapua
}

def run_all_scrapers(return_json=True):
    """Run all available scrapers and combine results"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Starting news scraping from all sources")
    logger.info("=" * 60)

    all_articles = []
    sources_found = []
    categories_found = set()
    site_results = {}

    regions_config = {
        'timika': 'timika',
        'mimika': 'mimika'
    }
    
    # We will track processed URLs to prevent duplicates if they appear in both searches
    processed_urls = set()

    for region_name, search_keyword in regions_config.items():
        logger.info(f"--- Scraping Region: {region_name.upper()} (Keyword: {search_keyword}) ---")
        
        for site_name, scraper_func in SCRAPERS.items():
            logger.info(f"Scraping {site_name} for {region_name}...")
            try:
                # Pass the keyword to the scraper
                # Note: Some scrapers might not support arg yet, need to ensuring all do or handle TypeError
                try:
                    result = scraper_func(keyword=search_keyword)
                except TypeError:
                    # Fallback for scrapers that don't accept keyword yet
                    result = scraper_func()
                
                articles = []
                
                # All scrapers now return dicts
                if isinstance(result, dict):
                    if result.get('status') == 'success' and result.get('data'):
                        articles = result['data'].get('articles', [])
                
                if articles:
                    # Enrich with region tag
                    for article in articles:
                        article['region'] = region_name
                        
                        # Only add if not seen (or maybe we want to allow dual-tagging? For now strict unique by URL)
                        # If a URL is already seen, it means it was found in previous region loop.
                        # We might want to keep the first finding or update it. 
                        # Let's simple append for now and handle uniqueness later or let Set handle it.
                        all_articles.append(article)

                    sources_found.append(f"{site_name} ({region_name})")

                    # Collect categories
                    for article in articles:
                        category = article.get('category', 'news')
                        categories_found.add(category)

                    logger.info(f"Successfully scraped {len(articles)} articles from {site_name} for {region_name}")
                    
                    # Update site results (cumulative count)
                    current_count = site_results.get(site_name, {}).get('count', 0)
                    site_results[site_name] = {'status': 'success', 'count': current_count + len(articles)}
                else:
                    logger.warning(f"No articles found from {site_name} for {region_name}")
            except Exception as e:
                logger.error(f"Error scraping {site_name} for {region_name}: {str(e)}")
                continue

    # Remove duplicates
    unique_articles = remove_duplicates(all_articles)
    logger.info(f"Total unique articles: {len(unique_articles)}")

    return {
        'status': 'success',
        'data': {
            'metadata': {
                'total_articles': len(unique_articles),
                'last_updated': datetime.now().isoformat(),
                'sources': sources_found,
                'categories': sorted(list(categories_found))
            },
            'articles': unique_articles
        },
        'site_results': site_results
    }

def run_specific_scraper(site_name, return_json=True):
    """Run scraper for specific site"""
    logger = setup_logging()

    if site_name not in SCRAPERS:
        error_msg = f"Unknown site: {site_name}"
        logger.error(error_msg)
        return {
            'status': 'error',
            'message': error_msg,
            'timestamp': datetime.now().isoformat()
        }

    logger.info(f"Scraping {site_name}...")
    try:
        result = SCRAPERS[site_name]()
        return result
    except Exception as e:
        error_msg = f"Error scraping {site_name}: {str(e)}"
        logger.error(error_msg)
        return {
            'status': 'error',
            'message': error_msg,
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main function with CLI interface"""
    parser = argparse.ArgumentParser(description='Indonesian News Scraper')
    parser.add_argument('--site', type=str, choices=list(SCRAPERS.keys()), help='Scrape specific site only')
    parser.add_argument('--list', action='store_true', help='List available scrapers')

    args = parser.parse_args()

    if args.list:
        print("Available scrapers:")
        for site in SCRAPERS.keys():
            print(f"  - {site}")
        return

    if args.site:
        result = run_specific_scraper(args.site)
    else:
        result = run_all_scrapers()

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()