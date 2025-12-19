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
from scrapers.kompas_scraper import scrape_kompas
from scrapers.cnn_scraper import scrape_cnn
from scrapers.antara_scraper import scrape_antara
from scrapers.narasi_scraper import scrape_narasi
from scrapers.tribun_scraper import scrape_tribun
from scrapers.detik_scraper import scrape_detik

from utils.helpers import setup_logging, remove_duplicates

# Configuration
SCRAPERS = {
    'detik': scrape_detik,
    'kompas': scrape_kompas,
    'cnn': scrape_cnn,
    'antara': scrape_antara,
    'narasi': scrape_narasi,
    'tribun': scrape_tribun
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

    for site_name, scraper_func in SCRAPERS.items():
        logger.info(f"Scraping {site_name}...")
        try:
            result = scraper_func()
            articles = []
            
            # All scrapers now return dicts
            if isinstance(result, dict):
                if result.get('status') == 'success' and result.get('data'):
                    articles = result['data'].get('articles', [])
            
            if articles:
                all_articles.extend(articles)
                sources_found.append(site_name.title())

                # Collect categories
                for article in articles:
                    category = article.get('category', 'news')
                    categories_found.add(category)

                logger.info(f"Successfully scraped {len(articles)} articles from {site_name}")
                site_results[site_name] = {'status': 'success', 'count': len(articles)}
            else:
                logger.warning(f"No articles found from {site_name}")
                site_results[site_name] = {'status': 'no_articles', 'count': 0}
        except Exception as e:
            logger.error(f"Error scraping {site_name}: {str(e)}")
            site_results[site_name] = {'status': 'error', 'error': str(e), 'count': 0}
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