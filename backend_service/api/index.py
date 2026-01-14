"""
Indonesian News Scraper API
Single-file API with integrated main.py scraper logic
All endpoints use centralized scraping functions from main.py
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

# ============= INITIALIZATION =============

app = FastAPI(
    title="📰 Indonesian News Scraper API",
    description="API untuk scraping berita dari situs berita utama Indonesia menggunakan single-file architecture",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ============= DATA MODELS =============

class ArticleResponse(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None

# ============= HELPER FUNCTIONS =============

def get_scrape_response(site_name=None):
    """Generic function to get scraper response using main.py logic"""

    # Enable CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        # Import main scraper functions
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from main import run_all_scrapers, run_specific_scraper

        # Use appropriate function based on site_name
        if site_name is None:
            # Scrape all sites
            response_data = run_all_scrapers(return_json=True)
        else:
            # Scrape specific site
            response_data = run_specific_scraper(site_name, return_json=True)

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

# ============= MAIN ENDPOINTS =============

@app.get("/", response_model=ArticleResponse)
async def get_news_data(
    search: Optional[str] = Query(None, description="Search articles by title or description"),
    source: Optional[str] = Query(None, description="Filter by news source"),
    category: Optional[str] = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page")
):
    """Get news data with filtering and pagination"""

    try:
        # Trigger real-time scrape instead of loading static data
        from main import run_all_scrapers
        result_data = run_all_scrapers(return_json=True)
        
        if result_data.get('status') == 'success':
            data = result_data.get('data', {})
        else:
            data = {"metadata": {}, "articles": []}
            
        articles = data.get('articles', [])

        # Apply filters
        if search:
            search_lower = search.lower()
            articles = [
                article for article in articles
                if search_lower in article.get('title', '').lower() or
                   search_lower in article.get('description', '').lower()
            ]

        if source:
            articles = [
                article for article in articles
                if source.lower() in article.get('source', '').lower()
            ]

        if category:
            articles = [
                article for article in articles
                if category.lower() in article.get('category', '').lower()
            ]

        # Pagination
        total = len(articles)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_articles = articles[start:end]

        return {
            "status": "success",
            "data": {
                "metadata": {
                    **data.get('metadata', {}),
                    "total_filtered": total,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": (total + per_page - 1) // per_page
                },
                "articles": paginated_articles
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api", response_model=ArticleResponse)
async def get_filtered_news(
    search: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Get filtered news (alias for main endpoint)"""
    return await get_news_data(search, source, category, page, per_page)

@app.get("/api/sources")
async def get_sources():
    """Get list of available news sources"""
    return {
        "status": "success",
        "data": {
            "sources": [
                {"id": "detik", "name": "Detik.com", "url": "https://www.detik.com"},
                {"id": "kompas", "name": "Kompas.com", "url": "https://www.kompas.com"},
                {"id": "cnn", "name": "CNN Indonesia", "url": "https://www.cnnindonesia.com"},
                {"id": "antara", "name": "Antara News", "url": "https://www.antaranews.com"},
                {"id": "tempo", "name": "Tempo", "url": "https://www.tempo.co"},
                {"id": "kumparan", "name": "Kumparan", "url": "https://www.kumparan.com"}
            ]
        }
    }

@app.get("/api/categories")
async def get_categories():
    """Get list of available categories (Requires live scrape)"""
    from main import run_all_scrapers
    result_data = run_all_scrapers(return_json=True)
    data = result_data.get('data', {})
    articles = data.get('articles', [])

    # Extract unique categories
    categories = set()
    for article in articles:
        if article.get('category'):
            categories.add(article['category'])

    return {
        "status": "success",
        "data": {
            "categories": sorted(list(categories))
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get statistics about the news data (Requires live scrape)"""
    from main import run_all_scrapers
    result_data = run_all_scrapers(return_json=True)
    data = result_data.get('data', {})
    metadata = data.get('metadata', {})
    articles = data.get('articles', [])

    # Calculate statistics
    source_counts = {}
    category_counts = {}

    for article in articles:
        # Count by source
        source = article.get('source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

        # Count by category
        category = article.get('category', 'news')
        category_counts[category] = category_counts.get(category, 0) + 1

    return {
        "status": "success",
        "data": {
            "total_articles": len(articles),
            "last_updated": metadata.get('last_updated'),
            "sources": source_counts,
            "categories": category_counts
        }
    }

@app.get("/api/refresh")
async def refresh_info():
    """Get refresh information"""
    return {
        "status": "success",
        "data": {
            "message": "Static data - use scrape endpoints for real-time data",
            "last_updated": datetime.now().isoformat(),
            "available_endpoints": [
                "/api/scrape/all",
                "/api/scrape/detik",
                "/api/scrape/kompas",
                "/api/scrape/cnn",
                "/api/scrape/antara",
                "/api/scrape/tempo",
                "/api/scrape/kumparan"
            ]
        }
    }

# ============= SCRAPER ENDPOINTS =============

@app.get("/api/scrape/status")
async def scrape_status():
    """Get scraper API documentation and status"""

    documentation = {
        "title": "Indonesian News Scraper API",
        "version": "2.0.0",
        "description": "Real-time scraping endpoints using integrated main.py logic",
        "architecture": "Single-file API with centralized scraper functions",
        "endpoints": {
            "real_time_scraping": {
                "/api/scrape/all": {
                    "method": "GET",
                    "description": "Scrape all news sites and return combined results",
                    "response": "JSON with all articles, metadata, and site-specific results"
                },
                "/api/scrape/detik": {
                    "method": "GET",
                    "description": "Scrape Detik.com only",
                    "response": "JSON with Detik.com articles and metadata"
                },
                "/api/scrape/kompas": {
                    "method": "GET",
                    "description": "Scrape Kompas.com only",
                    "response": "JSON with Kompas.com articles and metadata"
                },
                "/api/scrape/cnn": {
                    "method": "GET",
                    "description": "Scrape CNN Indonesia only",
                    "response": "JSON with CNN Indonesia articles and metadata"
                },
                "/api/scrape/antara": {
                    "method": "GET",
                    "description": "Scrape Antara News only",
                    "response": "JSON with Antara News articles and metadata"
                },
                "/api/scrape/tempo": {
                    "method": "GET",
                    "description": "Scrape Tempo only",
                    "response": "JSON with Tempo articles and metadata"
                },
                "/api/scrape/kumparan": {
                    "method": "GET",
                    "description": "Scrape Kumparan only",
                    "response": "JSON with Kumparan articles and metadata"
                }
            }
        },
        "flow_architecture": {
            "description": "Integrated scraping flow using main.py",
            "components": [
                "main.py - Central scraper logic with JSON return capability",
                "scrapers/ - Individual news site scrapers",
                "api/index.py - API endpoints using main.py functions",
                "Response - Direct JSON response (no file storage)"
            ],
            "advantages": [
                "✅ Single source of truth for scraping logic",
                "✅ No code duplication between CLI and API",
                "✅ Consistent data structure",
                "✅ Easy maintenance and updates"
            ]
        },
        "response_format": {
            "success": {
                "status": "success",
                "data": {
                    "metadata": {
                        "total_articles": "number",
                        "last_updated": "ISO timestamp",
                        "sources": ["source1", "source2"],
                        "categories": ["category1", "category2"],
                        "execution_time": "seconds (for individual scrapers)"
                    },
                    "articles": [
                        {
                            "title": "Article Title",
                            "url": "Article URL",
                            "description": "Article description",
                            "date": "Publication date",
                            "category": "Article category",
                            "source": "Source website"
                        }
                    ]
                },
                "site_results": {  # Only for /api/scrape/all
                    "sitename": {
                        "status": "success|no_articles|error",
                        "count": "number of articles",
                        "error": "error message (if applicable)"
                    }
                }
            },
            "error": {
                "status": "error",
                "message": "Error description",
                "timestamp": "ISO timestamp"
            }
        },
        "usage_examples": {
            "javascript": "fetch('https://your-app.vercel.app/api/scrape/all').then(r => r.json()).then(console.log)",
            "python": "requests.get('https://your-app.vercel.app/api/scrape/detik').json()",
            "curl": "curl https://your-app.vercel.app/api/scrape/all"
        }
    }

    return JSONResponse(
        content=documentation,
        headers={'Access-Control-Allow-Origin': '*'}
    )

@app.get("/api/scrape/all")
async def scrape_all_sites():
    """Scrape all news sites and return JSON response using main.py logic"""
    return get_scrape_response(site_name=None)

@app.get("/api/scrape/detik")
async def scrape_detik_endpoint():
    """Scrape Detik.com and return JSON response using main.py logic"""
    return get_scrape_response(site_name='detik')

@app.get("/api/scrape/kompas")
async def scrape_kompas_endpoint():
    """Scrape Kompas.com and return JSON response using main.py logic"""
    return get_scrape_response(site_name='kompas')

@app.get("/api/scrape/cnn")
async def scrape_cnn_endpoint():
    """Scrape CNN Indonesia and return JSON response using main.py logic"""
    return get_scrape_response(site_name='cnn')

@app.get("/api/scrape/antara")
async def scrape_antara_endpoint():
    """Scrape Antara News and return JSON response using main.py logic"""
    return get_scrape_response(site_name='antara')

@app.get("/api/scrape/tempo")
async def scrape_tempo_endpoint():
    """Scrape Tempo and return JSON response using main.py logic"""
    return get_scrape_response(site_name='tempo')

@app.get("/api/scrape/kumparan")
async def scrape_kumparan_endpoint():
    """Scrape Kumparan and return JSON response using main.py logic"""
    return get_scrape_response(site_name='kumparan')

# ============= UTILITY ENDPOINTS =============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Indonesian News Scraper API",
        "version": "2.0.0",
        "architecture": "Single-file with integrated main.py logic"
    }

# ============= ROOT HANDLER =============

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect to docs or serve static content"""
    return JSONResponse(
        content={
            "message": "📰 Indonesian News Scraper API",
            "version": "2.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "scrape_status": "/api/scrape/status",
            "static_data": "/?static=1",
            "real_time_scraping": {
                "all_sites": "/api/scrape/all",
                "detik": "/api/scrape/detik",
                "kompas": "/api/scrape/kompas",
                "cnn": "/api/scrape/cnn",
                "antara": "/api/scrape/antara",
                "tempo": "/api/scrape/tempo",
                "kumparan": "/api/scrape/kumparan"
            }
        },
        headers={'Access-Control-Allow-Origin': '*'}
    )

# ============= VERCEL HANDLER =============

def handler(request):
    """Vercel serverless function handler"""
    return app(request.scope, request.receive, request.send)

# Export for Vercel
handler.aws = handler