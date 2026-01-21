from fastapi import FastAPI, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, database
from pydantic import BaseModel
from datetime import datetime
from .utils.helpers import normalize_category

# Database creation moved to startup event

app = FastAPI(title="Papua News Backend API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Schemas ---
class ArticleCreate(BaseModel):
    title: str
    summary: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    source_url: str
    source_name: str
    category: str
    region: str = "general"
    published_at: Optional[datetime] = None

class ArticleResponse(ArticleCreate):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Papua News Backend API Running"}

@app.get("/articles", response_model=List[ArticleResponse])
def get_articles(
    db: Session = Depends(database.get_db),
    region: Optional[str] = Query(None, description="Filter by region (mimika/timika)"),
    x_region: Optional[str] = Header(None, alias="x-region"),
    limit: int = 1000
):
    """
    Get articles filtered by region.
    """
    effective_region = region or x_region
    
    query = db.query(models.Article)
    
    if effective_region:
        query = query.filter(models.Article.region.in_([effective_region, "general"]))
        if effective_region == "mimika":
             query = query.filter(models.Article.region != "timika")
        elif effective_region == "timika":
             query = query.filter(models.Article.region != "mimika")
    else:
        query = query.filter(models.Article.region == "general")

    return query.order_by(models.Article.published_at.desc()).limit(limit).all()

@app.get("/articles/{article_id}", response_model=ArticleResponse)
def read_article(
    article_id: int, 
    db: Session = Depends(database.get_db),
    x_region: Optional[str] = Header(None, alias="x-region")
):
    query = db.query(models.Article).filter(models.Article.id == article_id)
    
    # Enforce region isolation if header is present
    if x_region:
        if x_region == "mimika":
            query = query.filter(models.Article.region != "timika")
        elif x_region == "timika":
            query = query.filter(models.Article.region != "mimika")
            
    db_article = query.first()
    
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(database.get_db)):
    # 1. Validate Source
    ALLOWED_SOURCES = ["antara", "kompas", "detik", "papuanews", "seputarpapua"] # papuanews for internal/testing
    if article.source_name.lower() not in ALLOWED_SOURCES:
        raise HTTPException(status_code=400, detail=f"Source '{article.source_name}' is not allowed.")

    # 2. Deduplication check
    existing = db.query(models.Article).filter(models.Article.source_url == article.source_url).first()
    if existing:
        return existing
        
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


@app.post("/ingest/run")
def run_scraper_and_ingest(
    background_tasks: bool = Query(False, description="Run in background"), 
    db: Session = Depends(database.get_db),
    api_key: Optional[str] = Header(None, alias="x-api-key"),
    key: Optional[str] = Query(None)
):
    import os
    expected_secret = os.getenv("API_SECRET", "papua-news-secret-2024")
    if (api_key != expected_secret) and (key != expected_secret):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        from .services.scraper_engine import run_all_scrapers
        
        # Run scrapers (sync for now, better to be async or background task)
        scrape_result = run_all_scrapers(return_json=True)
        
        if scrape_result.get('status') != 'success':
            return {"status": "error", "message": "Scraper engine failed"}
            
        articles_data = scrape_result.get('data', {}).get('articles', [])
        saved_count = 0
        
        for article in articles_data:
            # Validate source
            from .utils.helpers import validate_source
            if not validate_source(article.get('url')):
                continue

            # Check for existing URL
            existing = db.query(models.Article).filter(models.Article.source_url == article['url']).first()
            if existing:
                # Update image if missing
                if not existing.image_url and article.get('image_url'):
                    existing.image_url = article.get('image_url')
                    db.add(existing)
                # Update category
                # Update category
                if article.get('category'):
                    normalized_cat = normalize_category(article.get('category'))
                    if existing.category in ["news", "News"] and normalized_cat != "Nasional":
                        existing.category = normalized_cat
                        db.add(existing)
                continue
                
            # Parse date
            published_at = datetime.now()
            try:
                if article.get('date'):
                    published_at = datetime.strptime(article['date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass # Use now() fallback
                
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
        
        return {
            "status": "success", 
            "articles_found": len(articles_data),
            "articles_saved": saved_count,
            "site_results": scrape_result.get('site_results', {})
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Ingest failed: {str(e)}"}

# --- Scheduler ---
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

scheduler = BackgroundScheduler()

def scheduled_scraper_job():
    """
    Wrapper for running the scraper in scheduler.
    Since scheduler runs in a separate thread, we need a new DB session.
    """
    print(f"[{datetime.now()}] Starting scheduled scraping...")
    db = database.SessionLocal()
    try:
        from .services.scraper_engine import run_all_scrapers
        
        # Run scrapers
        scrape_result = run_all_scrapers(return_json=True)
        
        if scrape_result.get('status') == 'success':
            articles_data = scrape_result.get('data', {}).get('articles', [])
            saved_count = 0
            
            for article_data in articles_data:
                # Validate source
                from .utils.helpers import validate_source
                if not validate_source(article_data.get('url')):
                    continue

                # Check for existing URL
                existing = db.query(models.Article).filter(models.Article.source_url == article_data['url']).first()
                if existing:
                    # Update image if missing and we found one
                    if not existing.image_url and article_data.get('image_url'):
                        existing.image_url = article_data.get('image_url')
                        db.add(existing) # Mark for update
                        print(f"Updated image for existing article: {existing.title}")
                    # Update category if it was "news" and we have better one
                    if existing.category == "news" and article_data.get('category') != "news":
                        existing.category = article_data.get('category')
                        db.add(existing)
                    # Update category
                    if article_data.get('category'):
                        normalized_cat = normalize_category(article_data.get('category'))
                        if existing.category in ["news", "News"] and normalized_cat != "Nasional":
                             existing.category = normalized_cat
                             db.add(existing)
                    continue
                    
                # Parse date
                published_at = datetime.now()
                try:
                    if article_data.get('date'):
                        published_at = datetime.strptime(article_data['date'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    pass 
                    
                new_article = models.Article(
                    title=article_data.get('title', 'No Title'),
                    summary=article_data.get('description', ''),
                    source_url=article_data.get('url', ''),
                    source_name=article_data.get('source', 'Unknown'),
                    category=normalize_category(article_data.get('category', 'news')),
                    region=article_data.get('region', 'general'),
                    image_url=article_data.get('image_url', None),
                    published_at=published_at
                )
                
                db.add(new_article)
                saved_count += 1
                
            db.commit()
            print(f"[{datetime.now()}] Scheduled scraping completed. Saved {saved_count} new articles.")
        else:
            print(f"[{datetime.now()}] Scheduled scraping failed: {scrape_result.get('message')}")
            
    except Exception as e:
        print(f"[{datetime.now()}] Error in scheduled scraper: {str(e)}")
    finally:
        db.close()

@app.on_event("startup")
def init_db():
    try:
        models.Base.metadata.create_all(bind=database.engine)
        print("Database tables created/verified successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.on_event("startup")
def start_scheduler():
    # Run every 30 minutes (Half-hourly) to accumulate data safely
    scheduler.add_job(
        scheduled_scraper_job,
        trigger=IntervalTrigger(minutes=30),
        id='scraper_job',
        name='Scrape News Every 30 Minutes',
        replace_existing=True
    )
    scheduler.start()
    print("Scheduler started. Scraping job registered (every 60 mins).")
    
    # Run immediately on startup (as requested)
    scheduler.add_job(
        scheduled_scraper_job,
        trigger='date',
        run_date=datetime.now(),
        id='startup_scraper',
        name='Startup Immediate Scrape'
    )
    print("Startup scrape scheduled to run immediately.")

@app.on_event("shutdown")
def shutdown_scheduler():
    scheduler.shutdown()

@app.get("/api/cron/scrape")
def vercel_cron_scrape():
    """
    Endpoint for Vercel Cron.
    """
    print(f"[{datetime.now()}] Vercel Cron triggered...")
    # Reuse the same job logic
    scheduled_scraper_job()
    return {"status": "success", "message": "Scraping job completed"}
