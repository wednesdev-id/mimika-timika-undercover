import sys
import os
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models, database
from app.services.scraper_engine import run_all_scrapers
from app.utils.helpers import normalize_category, validate_source

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def manual_ingest():
    logger.info("Starting manual ingestion...")
    
    # Create DB tables if they don't exist
    models.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    try:
        # Run scrapers
        scrape_result = run_all_scrapers(return_json=True)
        
        if scrape_result.get('status') != 'success':
            logger.error("Scraper failed")
            return
            
        articles_data = scrape_result.get('data', {}).get('articles', [])
        logger.info(f"Scraper found {len(articles_data)} articles in total.")
        
        saved_count = 0
        updated_count = 0
        
        for article in articles_data:
            # Validate source
            if not validate_source(article.get('url')):
                continue

            # Check for existing URL
            existing = db.query(models.Article).filter(models.Article.source_url == article['url']).first()
            if existing:
                # Update logic
                updated = False
                if not existing.image_url and article.get('image_url'):
                    existing.image_url = article.get('image_url')
                    updated = True
                
                normalized_cat = normalize_category(article.get('category'))
                if existing.category in ["news", "News"] and normalized_cat != "Nasional":
                    existing.category = normalized_cat
                    updated = True
                    
                if updated:
                    db.add(existing)
                    updated_count += 1
                continue
                
            # Parse date
            published_at = datetime.now()
            try:
                if article.get('date'):
                    # Try flexible parsing if needed, but scraper usually standardizes or helpers.extract_date does
                    # Here we assume scraper returns string, we try verification
                    try:
                        published_at = datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
                    except:
                        pass
            except ValueError:
                pass 
                
            new_article = models.Article(
                title=article.get('title', 'No Title'),
                summary=article.get('description', ''),
                source_url=article.get('url', ''),
                source_name=article.get('source', 'Unknown'),
                category=normalize_category(article.get('category', 'news')),
                region=article.get('region', 'general'),
                image_url=article.get('image_url', None),
                published_at=published_at
            )
            
            db.add(new_article)
            saved_count += 1
            
        db.commit()
        logger.info(f"Ingestion Complete. Saved: {saved_count}, Updated: {updated_count}")
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    manual_ingest()
