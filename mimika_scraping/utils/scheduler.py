"""
Scheduler for automatic news scraping
"""

import schedule
import time
import logging
from datetime import datetime
import argparse
from main import run_all_scrapers, run_specific_scraper
from utils.helpers import setup_logging

def schedule_daily_scraping(time_str="08:00"):
    """
    Schedule daily scraping at specified time
    Format: "HH:MM" in 24-hour format
    """
    logger = setup_logging()
    logger.info(f"Scheduling daily scraping at {time_str}")

    # Schedule daily scraping
    schedule.every().day.at(time_str).do(run_scheduled_scraping)

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def run_scheduled_scraping():
    """Function to be called by scheduler"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info(f"Starting scheduled scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    try:
        run_all_scrapers()
        logger.info("Scheduled scraping completed successfully")
    except Exception as e:
        logger.error(f"Scheduled scraping failed: {str(e)}")

def schedule_interval_scraping(minutes=60):
    """
    Schedule scraping at regular intervals
    Args:
        minutes: Interval in minutes between scrapes
    """
    logger = setup_logging()
    logger.info(f"Scheduling scraping every {minutes} minutes")

    # Schedule interval scraping
    schedule.every(minutes).minutes.do(run_scheduled_scraping)

    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler(mode='daily', time_str="08:00", interval=60):
    """
    Start the scheduler with specified mode
    Args:
        mode: 'daily' or 'interval'
        time_str: Time for daily mode (HH:MM)
        interval: Interval in minutes for interval mode
    """
    logger = setup_logging()
    logger.info(f"Starting news scraper scheduler in {mode} mode")

    if mode == 'daily':
        schedule_daily_scraping(time_str)
    elif mode == 'interval':
        schedule_interval_scraping(interval)
    else:
        logger.error(f"Unknown scheduler mode: {mode}")
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='News Scraper Scheduler')
    parser.add_argument('--mode', choices=['daily', 'interval'], default='daily',
                       help='Scheduler mode: daily or interval')
    parser.add_argument('--time', type=str, default='08:00',
                       help='Time for daily mode (HH:MM format)')
    parser.add_argument('--interval', type=int, default=60,
                       help='Interval in minutes for interval mode')

    args = parser.parse_args()

    try:
        start_scheduler(args.mode, args.time, args.interval)
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
    except Exception as e:
        print(f"Scheduler error: {str(e)}")