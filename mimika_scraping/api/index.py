"""
FastAPI Web Viewer for Indonesian News Scraper - Vercel Serverless Version
Displays JSON news data in a clean web interface with unified routing
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
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
        "message": "Use direct scraping endpoints instead: /api/scrape/all or /api/scrape/{site}",
        "available_endpoints": {
            "all": "/api/scrape/all",
            "detik": "/api/scrape/detik",
            "kompas": "/api/scrape/kompas",
            "cnn": "/api/scrape/cnn",
            "antara": "/api/scrape/antara",
            "narasi": "/api/scrape/narasi",
            "tribun": "/api/scrape/tribun"
        },
        "status": "use_direct_endpoints",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/scrape/status")
async def scrape_status():
    """Get information about available scraping endpoints"""
    return {
        "endpoints": {
            "all_sites": "/api/scrape/all - Scrape all news sites",
            "individual_sites": {
                "detik": "/api/scrape/detik",
                "kompas": "/api/scrape/kompas",
                "cnn": "/api/scrape/cnn",
                "antara": "/api/scrape/antara",
                "narasi": "/api/scrape/narasi",
                "tribun": "/api/scrape/tribun"
            }
        },
        "usage": {
            "method": "GET",
            "returns": "JSON response with articles",
            "caching": "Real-time scraping (no file storage)",
            "rate_limiting": "Consider server limits for production use"
        },
        "data_format": {
            "structure": {
                "status": "success|error",
                "data": {
                    "metadata": {
                        "total_articles": "number",
                        "last_updated": "ISO timestamp",
                        "sources": ["array of source names"],
                        "categories": ["array of categories"]
                    },
                    "articles": ["array of article objects"]
                },
                "site_results": "individual site performance (all endpoint only)"
            }
        },
        "article_structure": {
            "title": "Article title",
            "url": "Article URL",
            "description": "Article description",
            "date": "YYYY-MM-DD HH:MM:SS",
            "category": "News category",
            "source": "Source website"
        }
    }


# ============= SCRAPER ENDPOINTS =============

@app.get("/api/scrape/all")
async def scrape_all_sites():
    """Scrape all news sites and return JSON response"""

    # Enable CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        # Import all scrapers
        from scrapers.kompas_scraper import scrape_kompas
        from scrapers.cnn_scraper import scrape_cnn
        from scrapers.antara_scraper import scrape_antara
        from scrapers.narasi_scraper import scrape_narasi
        from scrapers.tribun_scraper import scrape_tribun
        from scrapers.detik_scraper import scrape_detik

        SCRAPERS = {
            'kompas': scrape_kompas,
            'cnn': scrape_cnn,
            'antara': scrape_antara,
            'narasi': scrape_narasi,
            'tribun': scrape_tribun,
            'detik': scrape_detik
        }

        all_articles = []
        sources_found = []
        categories_found = set()
        site_results = {}

        # Run all scrapers
        for site_name, scraper_func in SCRAPERS.items():
            try:
                print(f"Scraping {site_name}...")
                df = scraper_func()

                if not df.empty:
                    articles = df.to_dict('records')
                    all_articles.extend(articles)
                    sources_found.append(site_name.title())

                    # Collect categories
                    for article in articles:
                        category = article.get('category', 'news')
                        categories_found.add(category)

                    site_results[site_name] = {
                        'status': 'success',
                        'count': len(articles)
                    }
                else:
                    site_results[site_name] = {
                        'status': 'no_articles',
                        'count': 0
                    }

            except Exception as e:
                print(f"Error scraping {site_name}: {str(e)}")
                site_results[site_name] = {
                    'status': 'error',
                    'error': str(e),
                    'count': 0
                }

        # Remove duplicates based on URL
        unique_articles = []
        seen_urls = set()

        for article in all_articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)

        response_data = {
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

@app.get("/api/scrape/detik")
async def scrape_detik_endpoint():
    """Scrape Detik.com and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.detik_scraper import scrape_detik

        df = scrape_detik()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Detik.com'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            # Convert DataFrame to dict
            articles = df.to_dict('records')

            # Get unique categories
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Detik.com'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Detik scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

@app.get("/api/scrape/kompas")
async def scrape_kompas_endpoint():
    """Scrape Kompas.com and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.kompas_scraper import scrape_kompas

        df = scrape_kompas()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Kompas.com'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            articles = df.to_dict('records')
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Kompas.com'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Kompas scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

@app.get("/api/scrape/cnn")
async def scrape_cnn_endpoint():
    """Scrape CNN Indonesia and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.cnn_scraper import scrape_cnn

        df = scrape_cnn()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['CNN Indonesia'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            articles = df.to_dict('records')
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['CNN Indonesia'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'CNN scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

@app.get("/api/scrape/antara")
async def scrape_antara_endpoint():
    """Scrape Antara News and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.antara_scraper import scrape_antara

        df = scrape_antara()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Antara News'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            articles = df.to_dict('records')
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Antara News'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Antara scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

@app.get("/api/scrape/narasi")
async def scrape_narasi_endpoint():
    """Scrape Narasi and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.narasi_scraper import scrape_narasi

        df = scrape_narasi()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Narasi'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            articles = df.to_dict('records')
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Narasi'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Narasi scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

@app.get("/api/scrape/tribun")
async def scrape_tribun_endpoint():
    """Scrape Tribun News and return JSON response"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    try:
        from scrapers.tribun_scraper import scrape_tribun

        df = scrape_tribun()

        if df.empty:
            response_data = {
                'status': 'success',
                'message': 'No articles found',
                'data': {
                    'metadata': {
                        'total_articles': 0,
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Tribun News'],
                        'categories': []
                    },
                    'articles': []
                }
            }
        else:
            articles = df.to_dict('records')
            categories = list(set(article.get('category', 'news') for article in articles))

            response_data = {
                'status': 'success',
                'data': {
                    'metadata': {
                        'total_articles': len(articles),
                        'last_updated': datetime.now().isoformat(),
                        'sources': ['Tribun News'],
                        'categories': sorted(categories)
                    },
                    'articles': articles
                }
            }

        return JSONResponse(
            content=response_data,
            headers=headers,
            status_code=200
        )

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': f'Tribun scraping failed: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

        return JSONResponse(
            content=error_response,
            headers=headers,
            status_code=500
        )

# ============= HEALTH CHECK =============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "environment": "vercel"
    }


