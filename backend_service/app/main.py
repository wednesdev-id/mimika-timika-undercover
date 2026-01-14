from fastapi import FastAPI, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, database
from pydantic import BaseModel
from datetime import datetime

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Papua News Backend API")

# --- Schemas ---
class ArticleCreate(BaseModel):
    title: str
    summary: str
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
    limit: int = 50
):
    """
    Get articles filtered by region.
    Region can be passed via Query param `?region=mimika` or Header `x-region: mimika`.
    If no region is specified, returns all (or 'general' + 'all' logic depending on requirement).
    """
    effective_region = region or x_region
    
    query = db.query(models.Article)
    
    if effective_region:
        # Simple logic: If region is 'mimika', show 'mimika' AND 'general'. 
        # Or strict filtering. Let's do loose filtering for now.
        query = query.filter(models.Article.region.in_([effective_region, "general"]))
        
    return query.order_by(models.Article.published_at.desc()).limit(limit).all()

@app.post("/articles", response_model=ArticleResponse)
def create_article(article: ArticleCreate, db: Session = Depends(database.get_db)):
    # Check if exists
    existing = db.query(models.Article).filter(models.Article.source_url == article.source_url).first()
    if existing:
        return existing
        
    db_article = models.Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

@app.post("/ingest/run")
def run_scraper_and_ingest(background_tasks: bool = Query(False, description="Run in background"), db: Session = Depends(database.get_db)):
    """
    Trigger scraper and save results to DB.
    """
    try:
        from .services.scraper_engine import run_all_scrapers
        
        # Run scrapers (sync for now, better to be async or background task)
        scrape_result = run_all_scrapers(return_json=True)
        
        if scrape_result.get('status') != 'success':
            return {"status": "error", "message": "Scraper engine failed"}
            
        articles_data = scrape_result.get('data', {}).get('articles', [])
        saved_count = 0
        
        for article in articles_data:
            # Check for existing URL
            existing = db.query(models.Article).filter(models.Article.source_url == article['url']).first()
            if existing:
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
                category=article.get('category', 'news'),
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
        
    except ImportError as e:
        return {"status": "error", "message": f"Import failed: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Ingest failed: {str(e)}"}
