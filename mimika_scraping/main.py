"""
Main News Scraper Application
"""

import pandas as pd
import argparse
import logging
import os
import sys
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

# Import utilities
from utils.helpers import setup_logging, save_to_csv, save_to_excel, save_to_json, remove_duplicates

# Load environment variables
load_dotenv()

# Available scrapers
SCRAPERS = {
    'kompas': scrape_kompas,
    'cnn': scrape_cnn,
    'antara': scrape_antara,
    'narasi': scrape_narasi,
    'tribun': scrape_tribun,
    'detik': scrape_detik
}

def run_all_scrapers(return_json=False):
    """Run all available scrapers and combine results

    Args:
        return_json (bool): If True, return JSON response instead of saving to file

    Returns:
        dict: JSON response if return_json=True
        str: Filename if return_json=False and articles found
        None: If no articles found and return_json=False
    """
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
            
            # Handle dict response
            if isinstance(result, dict):
                if result.get('status') == 'success' and result.get('data'):
                    articles = result['data'].get('articles', [])
            
            # Handle DataFrame response
            elif hasattr(result, 'empty'):
                if not result.empty:
                    articles = result.to_dict('records')
            
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

    # Return JSON response if requested
    if return_json:
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
    
    # If not returning JSON (CLI mode), just return the articles
    return unique_articles if unique_articles else []

def run_specific_scraper(site_name, return_json=False):
    """Run scraper for specific site

    Args:
        site_name (str): Name of the site to scrape
        return_json (bool): If True, return JSON response instead of saving to file

    Returns:
        dict: JSON response if return_json=True
        str: Filename if return_json=False and articles found
        None: If no articles found or error
    """
    logger = setup_logging()

    if site_name not in SCRAPERS:
        error_msg = f"Unknown site: {site_name}"
        logger.error(error_msg)
        logger.info(f"Available sites: {', '.join(SCRAPERS.keys())}")

        if return_json:
            return {
                'status': 'error',
                'message': error_msg,
                'available_sites': list(SCRAPERS.keys())
            }
        return None

    logger.info(f"Scraping {site_name}...")
    try:
        result = SCRAPERS[site_name]()
        
        # Handle dict response (new format)
        if isinstance(result, dict):
            # If return_json is True, return as-is
            if return_json:
                return result
            
            # Always return result directly without saving to file
            return result
        
        # Handle DataFrame response (legacy scrapers)
        elif hasattr(result, 'empty'):
            df = result
            if not df.empty:
                articles = df.to_dict('records')

                # Always return data structure directly
                categories = list(set(article.get('category', 'news') for article in articles))
                return {
                    'status': 'success',
                    'data': {
                        'metadata': {
                            'total_articles': len(articles),
                            'last_updated': datetime.now().isoformat(),
                            'sources': [site_name.title()],
                            'categories': sorted(categories)
                        },
                        'articles': articles
                    }
                }
            else:
                warning_msg = f"No articles found from {site_name}"
                logger.warning(warning_msg)

                return {
                    'status': 'success',
                    'message': warning_msg,
                    'data': {
                        'metadata': {
                            'total_articles': 0,
                            'last_updated': datetime.now().isoformat(),
                            'sources': [site_name.title()],
                            'categories': []
                        },
                        'articles': []
                    }
                }
    except Exception as e:
        error_msg = f"Error scraping {site_name}: {str(e)}"
        logger.error(error_msg)

        if return_json:
            return {
                'status': 'error',
                'message': error_msg,
                'timestamp': datetime.now().isoformat()
            }
        return None

def run_scheduler():
    """Run the scheduler in background"""
    from utils.scheduler import start_scheduler

    logger = setup_logging()
    logger.info("Starting news scraper scheduler...")

    # Get scheduler settings from environment
    scheduler_mode = os.getenv('SCHEDULER_MODE', 'daily')
    scheduler_time = os.getenv('SCHEDULER_TIME', '08:00')
    scheduler_interval = int(os.getenv('SCHEDULER_INTERVAL', '60'))

    try:
        start_scheduler(scheduler_mode, scheduler_time, scheduler_interval)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")

def main():
    """Main function with CLI interface"""
    parser = argparse.ArgumentParser(description='Indonesian News Scraper')

    parser.add_argument('--site', type=str, choices=list(SCRAPERS.keys()),
                    help='Scrape specific site only')
    parser.add_argument('--format', type=str, choices=['json', 'csv', 'excel'], default='json',
                    help='Output format (default: json)')
    parser.add_argument('--scheduler', action='store_true',
                    help='Run scheduler instead of one-time scraping')
    parser.add_argument('--list', action='store_true',
                    help='List available scrapers')

    args = parser.parse_args()

    # Set output format
    os.environ['OUTPUT_FORMAT'] = args.format

    if args.list:
        print("Available scrapers:")
        for site in SCRAPERS.keys():
            print(f"  - {site}")
        return

    if args.scheduler:
        run_scheduler()
    elif args.site:
        result = run_specific_scraper(args.site, return_json=True)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"status": "error", "message": "Scraping failed"}, indent=2))
    else:
        # Default: scrape all
        result = run_all_scrapers(return_json=True)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(json.dumps({"status": "no_articles", "message": "No articles found"}, indent=2))

if __name__ == "__main__":
    main()