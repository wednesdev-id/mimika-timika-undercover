"""
FastAPI Web Viewer for Indonesian News Scraper - Vercel Serverless Version
Displays JSON news data in a clean web interface with unified routing
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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
TEMPLATES_DIR = BASE_DIR / 'templates'

# Templates setup - with error handling for serverless
try:
    templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
except Exception:
    # Fallback for serverless environments
    templates = None

# Mount static files
try:
    app.mount("/static", StaticFiles(directory=str(BASE_DIR / 'static')), name="static")
except RuntimeError:
    # Static files mounting may fail in serverless environment
    pass

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
print("File exists?", SAMPLE_DATA.exists())

def load_latest_json_data() -> Dict[str, Any]:
    """Load the most recent JSON data file or return sample data"""
    try:
        if not DATA_DIR.exists():
            return SAMPLE_DATA

        json_files = [f for f in DATA_DIR.glob('*.json')]
        if not json_files:
            return SAMPLE_DATA

        # Sort by filename (which includes date) to get the latest
        latest_file = sorted(json_files)[-1]

        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return SAMPLE_DATA

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

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main page with news display"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    # Get filter parameters from query
    filters = {
        'search': request.query_params.get('search', ''),
        'source': request.query_params.get('source', 'all'),
        'category': request.query_params.get('category', 'all')
    }

    # Apply filters
    filtered_articles = filter_articles(articles, filters)

    # Get unique sources and categories for dropdowns
    sources = list(set(article.get('source', 'Unknown') for article in articles))
    categories = list(set(article.get('category', 'Unknown') for article in articles))

    # Sort by date (newest first)
    filtered_articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Handle template rendering with fallback
    if templates is None:
        # Fallback HTML response for serverless environments
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Papua News Viewer</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
                .article {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; transition: box-shadow 0.3s; }}
                .article:hover {{ box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .title {{ color: #2c3e50; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
                .meta {{ color: #666; font-size: 12px; margin-bottom: 12px; }}
                .description {{ color: #333; line-height: 1.6; margin-bottom: 15px; }}
                .header {{ text-align: center; background: #3498db; color: white; padding: 20px; margin: -20px -20px 20px -20px; border-radius: 10px 10px 0 0; }}
                .nav-links {{ text-align: center; margin: 20px 0; }}
                .nav-links a {{ color: #3498db; text-decoration: none; margin: 0 15px; font-weight: bold; }}
                .stats {{ background: #2c3e50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center; }}
                .read-more {{ color: #3498db; text-decoration: none; font-weight: bold; }}
                .read-more:hover {{ text-decoration: underline; }}
                .tags {{ margin-top: 10px; }}
                .tag {{ background: #3498db; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; margin-right: 5px; display: inline-block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📰 Papua News Viewer</h1>
                    <p>Latest news from Papua sources</p>
                    <p>Last Updated: {metadata.get('last_updated', 'Unknown')}</p>
                </div>

                <div class="nav-links">
                    <a href="/articles">View All Articles →</a>
                    <a href="/docs">API Documentation</a>
                    <a href="/api/stats">Statistics</a>
                </div>

                <div class="stats">
                    <strong>Total Articles:</strong> {len(filtered_articles)} |
                    <strong>Sources:</strong> {len(set(article.get('source', 'Unknown') for article in articles))} |
                    <strong>Categories:</strong> {len(set(article.get('category', 'Unknown') for article in articles))}
                </div>
        """

        # Show all articles (not just first 10)
        for article in filtered_articles:
            title = article.get('title', 'No Title')
            description = article.get('description', 'No description available')
            url = article.get('url', '#')
            source = article.get('source', 'Unknown')
            category = article.get('category', 'Unknown')
            date = article.get('date', 'Unknown')[:19].replace('T', ' ')
            tags = article.get('tags', [])

            html_content += f"""
                <div class="article">
                    <div class="title">{title}</div>
                    <div class="meta">
                        <strong>Source:</strong> {source} |
                        <strong>Category:</strong> {category} |
                        <strong>Date:</strong> {date}
                    </div>
                    <div class="description">{description}</div>
            """

            if tags:
                html_content += '<div class="tags">'
                for tag in tags:
                    html_content += f'<span class="tag">{tag}</span>'
                html_content += '</div>'

            html_content += f"""
                    <div style="margin-top: 15px;">
                        <a href="{url}" target="_blank" class="read-more">Read Full Article →</a>
                    </div>
                </div>
            """

        html_content += f"""
            </div>
            <div style="text-align: center; margin-top: 40px; color: #666; font-size: 14px;">
                <p>🚀 Papua News Viewer - Powered by FastAPI</p>
                <p>Deployed on Vercel with serverless functions</p>
                <p><a href="/articles" target="_blank">View All Articles ({len(filtered_articles)} total)</a> | <a href="/docs" target="_blank">API Documentation</a></p>
                <p style="margin-top: 20px; font-size: 12px;">
                    Data source: {SAMPLE_DATA.name if SAMPLE_DATA.exists() else 'No data file found'}
                </p>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "articles": filtered_articles,
            "metadata": metadata,
            "sources": sorted(sources),
            "categories": sorted(categories),
            "filters": filters,
            "total_filtered": len(filtered_articles)
        })

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

# Health check endpoint
@app.get("/articles", response_class=HTMLResponse)
async def articles_page(request: Request):
    """Dedicated page to display all scraped news articles"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    # Get filter parameters from query
    filters = {
        'search': request.query_params.get('search', ''),
        'source': request.query_params.get('source', 'all'),
        'category': request.query_params.get('category', 'all')
    }

    # Apply filters
    filtered_articles = filter_articles(articles, filters)

    # Get unique sources and categories for dropdowns
    sources = list(set(article.get('source', 'Unknown') for article in articles))
    categories = list(set(article.get('category', 'Unknown') for article in articles))

    # Sort by date (newest first)
    filtered_articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    # Handle template rendering with fallback
    if templates is None:
        # Fallback HTML response for serverless environments
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>All Articles - Indonesian News Viewer</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; background: #e74c3c; color: white; padding: 20px; margin: -20px -20px 20px -20px; border-radius: 10px 10px 0 0; }}
                .filters {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .filter-group {{ display: inline-block; margin: 10px; }}
                .filter-group label {{ display: block; font-weight: bold; margin-bottom: 5px; }}
                .filter-group input, .filter-group select {{ padding: 8px; border: 1px solid #bdc3c7; border-radius: 3px; width: 200px; }}
                .article {{ border: 1px solid #ddd; margin: 15px 0; padding: 20px; border-radius: 8px; transition: box-shadow 0.3s; }}
                .article:hover {{ box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .title {{ color: #2c3e50; font-size: 20px; font-weight: bold; margin-bottom: 10px; }}
                .meta {{ color: #666; font-size: 12px; margin-bottom: 12px; }}
                .description {{ color: #333; line-height: 1.6; margin-bottom: 15px; }}
                .tags {{ margin-top: 10px; }}
                .tag {{ background: #3498db; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; margin-right: 5px; display: inline-block; }}
                .read-more {{ color: #e74c3c; text-decoration: none; font-weight: bold; }}
                .read-more:hover {{ text-decoration: underline; }}
                .stats {{ background: #2c3e50; color: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; text-align: center; }}
                .nav-links {{ text-align: center; margin: 20px 0; }}
                .nav-links a {{ color: #e74c3c; text-decoration: none; margin: 0 15px; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📰 All Articles</h1>
                    <p>Complete collection of scraped news from Papua sources</p>
                </div>

                <div class="nav-links">
                    <a href="/">← Back to Home</a>
                    <a href="/docs">API Documentation</a>
                    <a href="/api/stats">Statistics</a>
                </div>

                <div class="stats">
                    <strong>Total Articles:</strong> {len(filtered_articles)} |
                    <strong>Sources:</strong> {len(sources)} |
                    <strong>Categories:</strong> {len(categories)}
                </div>

                <div class="filters">
                    <div class="filter-group">
                        <label for="search">Search:</label>
                        <input type="text" id="search" name="search" value="{filters['search']}" placeholder="Search in titles and descriptions...">
                    </div>
                    <div class="filter-group">
                        <label for="source">Source:</label>
                        <select id="source" name="source">
                            <option value="all" {'selected' if filters['source'] == 'all' else ''}>All Sources</option>
        """

        # Add source options
        for source in sorted(sources):
            selected = 'selected' if filters['source'] == source else ''
            html_content += f'<option value="{source}" {selected}>{source}</option>'

        html_content += f"""
                        </select>
                    </div>
                    <div class="filter-group">
                        <label for="category">Category:</label>
                        <select id="category" name="category">
                            <option value="all" {'selected' if filters['category'] == 'all' else ''}>All Categories</option>
        """

        # Add category options
        for category in sorted(categories):
            selected = 'selected' if filters['category'] == category else ''
            html_content += f'<option value="{category}" {selected}>{category}</option>'

        html_content += """
                        </select>
                    </div>
                    <div class="filter-group">
                        <label>&nbsp;</label>
                        <button type="submit" style="padding: 8px 20px; background: #e74c3c; color: white; border: none; border-radius: 3px; cursor: pointer;">Apply Filters</button>
                    </div>
                </div>
        """

        # Display all articles
        for article in filtered_articles:
            title = article.get('title', 'No Title')
            description = article.get('description', 'No description available')
            url = article.get('url', '#')
            source = article.get('source', 'Unknown')
            category = article.get('category', 'Unknown')
            date = article.get('date', 'Unknown')[:19].replace('T', ' ')
            author = article.get('author', 'Unknown')
            tags = article.get('tags', [])

            html_content += f"""
                <div class="article">
                    <div class="title">{title}</div>
                    <div class="meta">
                        <strong>Source:</strong> {source} |
                        <strong>Category:</strong> {category} |
                        <strong>Date:</strong> {date} |
                        <strong>Author:</strong> {author}
                    </div>
                    <div class="description">{description}</div>
            """

            if tags:
                html_content += '<div class="tags">'
                for tag in tags:
                    html_content += f'<span class="tag">{tag}</span>'
                html_content += '</div>'

            html_content += f"""
                    <div style="margin-top: 15px;">
                        <a href="{url}" target="_blank" class="read-more">Read Full Article →</a>
                    </div>
                </div>
            """

        # Add footer with data source info
        data_source_name = SAMPLE_DATA.name if SAMPLE_DATA.exists() else 'No data file found'
        last_scraped = metadata.get('scraped_at', 'Unknown')

        html_content += f"""
            </div>

            <div style="text-align: center; margin-top: 40px; color: #666; font-size: 12px; border-top: 1px solid #ddd; padding-top: 20px;">
                <p>📄 Data source: {data_source_name}</p>
                <p>Last scraped: {last_scraped}</p>
                <p>🚀 Papua News Viewer - Powered by FastAPI on Vercel</p>
            </div>
        </body>
        </html>
        """

        # Add JavaScript separately to avoid f-string conflicts
        html_content += """
        <script>
            // Auto-submit form when filters change
            document.querySelectorAll('input, select').forEach(function(element) {
                element.addEventListener('change', function() {
                    if (this.id !== 'search' || this.value.length > 2 || this.value.length === 0) {
                        window.location.href = window.location.pathname + '?' + new URLSearchParams(new FormData(this.closest('form'))).toString();
                    }
                });
            });

            // Debounce search input
            let searchTimeout;
            document.getElementById('search').addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    if (this.value.length > 2 || this.value.length === 0) {
                        window.location.href = window.location.pathname + '?' + new URLSearchParams(new FormData(this.closest('form'))).toString();
                    }
                }, 500);
            });
        </script>
        """
        return HTMLResponse(content=html_content)
    else:
        return templates.TemplateResponse("articles.html", {
            "request": request,
            "articles": filtered_articles,
            "metadata": metadata,
            "sources": sorted(sources),
            "categories": sorted(categories),
            "filters": filters,
            "total_filtered": len(filtered_articles),
            "total_sources": len(sources),
            "total_categories": len(categories)
        })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "environment": "vercel"
    }

