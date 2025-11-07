"""
FastAPI Web Viewer for Indonesian News Scraper - Vercel Serverless Version
Displays JSON news data in a clean web interface with unified routing
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from pathlib import Path

# Initialize FastAPI app for serverless
app = FastAPI(
    title="Indonesian News API",
    description="API for Indonesian news scraper with web interface",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Data directory - adjust for Vercel environment
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'


# Pydantic models for API
class ArticleResponse(BaseModel):
    articles: List[Dict[str, Any]]
    total: int
    pagination: Optional[Dict[str, Any]] = None

class FilterParams(BaseModel):
    search: Optional[str] = None
    source: Optional[str] = "all"
    category: Optional[str] = "all"
    page: int = 1
    per_page: int = 20
    all: bool = False

# Sample data for initial deployment when no data files exist
SAMPLE_DATA = Path(__file__).resolve().parent.parent / "data" / "news_detik_20251105.json"
TARGET_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "news_detik_20251105.json"
print("File exists?", TARGET_DATA_FILE.exists())

def load_latest_json_data() -> Dict[str, Any]:
    """Load data from the specified JSON file"""
    try:
        # Always use the target data file as requested
        if TARGET_DATA_FILE.exists():
            print(f"Loading data from: {TARGET_DATA_FILE}")
            with open(TARGET_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Target file {TARGET_DATA_FILE} not found, using fallback")
            with open(SAMPLE_DATA, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        try:
            with open(SAMPLE_DATA, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e2:
            print(f"Error loading sample data: {e2}")
            return {"metadata": {"total_articles": 0, "error": "Failed to load any data"}, "articles": []}

def filter_articles(articles: List[Dict], filters: Dict) -> List[Dict]:
    """Filter articles based on search criteria"""
    filtered = articles

    # Search by keyword
    if filters.get('search'):
        search_term = filters['search'].lower()
        filtered = [a for a in filtered
                   if search_term in a.get('title', '').lower()
                   or search_term in a.get('description', '').lower()]

    # Filter by source
    if filters.get('source') and filters['source'] != 'all':
        filtered = [a for a in filtered if a.get('source') == filters['source']]

    # Filter by category
    if filters.get('category') and filters['category'] != 'all':
        filtered = [a for a in filtered if a.get('category') == filters['category']]

    return filtered

@app.get("/")
async def root():
    """Main page - return JSON data directly"""
    return load_latest_json_data()

@app.get("/json")
async def get_json_data():
    """Return JSON data from the specified file"""
    data = load_latest_json_data()
    return JSONResponse(content=data)

@app.get("/api", response_model=ArticleResponse)
async def get_articles(
    search: Optional[str] = Query(None, description="Search keywords in title or description"),
    source: Optional[str] = Query("all", description="Filter by news source"),
    category: Optional[str] = Query("all", description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    all: bool = Query(False, description="Return all articles without pagination")
):
    """
    Get articles with filtering and pagination options

    - **search**: Search for keywords in title or description
    - **source**: Filter by specific news source (use 'all' for all sources)
    - **category**: Filter by category (use 'all' for all categories)
    - **page**: Page number for pagination (default: 1)
    - **per_page**: Number of articles per page (default: 20, max: 100)
    - **all**: Set to True to return all articles without pagination
    """

    data = load_latest_json_data()
    articles = data.get('articles', [])

    # Apply filters
    filters = {
        'search': search,
        'source': source,
        'category': category
    }
    filtered_articles = filter_articles(articles, filters)

    if all:
        # Return all articles without pagination
        return ArticleResponse(
            articles=filtered_articles,
            total=len(filtered_articles),
            pagination=None
        )

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = filtered_articles[start:end]

    pagination_info = {
        "page": page,
        "per_page": per_page,
        "total": len(filtered_articles),
        "pages": (len(filtered_articles) + per_page - 1) // per_page
    }

    return ArticleResponse(
        articles=paginated_articles,
        total=len(filtered_articles),
        pagination=pagination_info
    )

@app.get("/api/sources")
async def get_sources():
    """Get list of available news sources"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    sources = list(set(article.get('source', 'Unknown') for article in articles))

    return {
        "sources": sorted(sources),
        "total": len(sources)
    }

@app.get("/api/categories")
async def get_categories():
    """Get list of available categories"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    categories = list(set(article.get('category', 'Unknown') for article in articles))

    return {
        "categories": sorted(categories),
        "total": len(categories)
    }

@app.get("/api/stats")
async def get_stats():
    """Get statistics about the news data"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    # Calculate additional stats
    sources = list(set(article.get('source', 'Unknown') for article in articles))
    categories = list(set(article.get('category', 'Unknown') for article in articles))

    # Count articles by source
    source_counts = {}
    for article in articles:
        source = article.get('source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

    # Count articles by category
    category_counts = {}
    for article in articles:
        category = article.get('category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1

    return {
        "metadata": metadata,
        "total_articles": len(articles),
        "total_sources": len(sources),
        "total_categories": len(categories),
        "sources": sources,
        "categories": categories,
        "source_distribution": source_counts,
        "category_distribution": category_counts,
        "latest_date": max([article.get('date', '') for article in articles]) if articles else None
    }

@app.get("/api/refresh")
async def refresh_data():
    """Trigger data refresh (placeholder for Vercel)"""
    return {
        "message": "Data refresh functionality requires a backend service. Consider using Railway, Render, or PythonAnywhere for full functionality.",
        "status": "limited_on_vercel",
        "timestamp": datetime.now().isoformat(),
        "alternatives": [
            "Railway.app",
            "Render.com",
            "PythonAnywhere.com",
            "Heroku"
        ]
    }

@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    """Web UI showing 50 articles"""
    data = load_latest_json_data()
    all_articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    # Take only first 50 articles
    articles = all_articles[:50]

    # Sort by date (newest first)
    articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Papua News Viewer - 50 Articles</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
            .header {{ text-align: center; background: #e74c3c; color: white; padding: 20px; margin: -20px -20px 20px -20px; border-radius: 10px 10px 0 0; }}
            .stats {{ background: #2c3e50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center; }}
            .nav-links {{ text-align: center; margin: 20px 0; }}
            .nav-links a {{ color: #e74c3c; text-decoration: none; margin: 0 15px; font-weight: bold; }}
            .article {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; transition: box-shadow 0.3s; }}
            .article:hover {{ box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .title {{ color: #2c3e50; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
            .meta {{ color: #666; font-size: 12px; margin-bottom: 12px; }}
            .description {{ color: #333; line-height: 1.6; margin-bottom: 15px; }}
            .read-more {{ color: #e74c3c; text-decoration: none; font-weight: bold; }}
            .read-more:hover {{ text-decoration: underline; }}
            .footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📰 Papua News Viewer</h1>
                <p>Showing 50 latest articles from Detik.com</p>
            </div>

            <div class="nav-links">
                <a href="/">📄 Full JSON API</a>
                <a href="/docs">API Documentation</a>
                <a href="/api/stats">Statistics</a>
            </div>

            <div class="stats">
                <strong>Showing:</strong> {len(articles)} of {len(all_articles)} articles |
                <strong>Source:</strong> Detik.com |
                <strong>Full Data:</strong> <a href="/">Available here</a>
            </div>
    """

    # Display articles
    for article in articles:
        title = article.get('title', 'No Title')
        description = article.get('description', 'No description available')
        url = article.get('url', '#')
        source = article.get('source', 'Unknown')
        date = article.get('date', 'Unknown')[:10]

        html_content += f"""
            <div class="article">
                <div class="title">{title}</div>
                <div class="meta">
                    <strong>Source:</strong> {source} |
                    <strong>Date:</strong> {date}
                </div>
                <div class="description">{description}</div>
                <div style="margin-top: 15px;">
                    <a href="{url}" target="_blank" class="read-more">Read Full Article →</a>
                </div>
            </div>
        """

    html_content += f"""
            <div class="footer">
                <p>📄 Data source: {TARGET_DATA_FILE.name}</p>
                <p>Last updated: {metadata.get('last_updated', 'Unknown')}</p>
                <p>🚀 For complete data ({len(all_articles)} articles), visit <a href="/">Root API</a></p>
                <p>🤖 Powered by FastAPI on Vercel</p>
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "environment": "vercel"
    }

