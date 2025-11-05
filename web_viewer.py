"""
Web Viewer for Indonesian News Scraper
Displays JSON news data in a clean web interface
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from typing import List, Dict, Any

app = Flask(__name__)

# Data directory
DATA_DIR = 'data'

def load_latest_json_data() -> Dict[str, Any]:
    """Load the most recent JSON data file"""
    try:
        json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        if not json_files:
            return {"metadata": {"total_articles": 0}, "articles": []}

        # Sort by filename (which includes date) to get the latest
        latest_file = sorted(json_files)[-1]
        file_path = os.path.join(DATA_DIR, latest_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return {"metadata": {"total_articles": 0}, "articles": []}

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

@app.route('/')
def index():
    """Main page with news display"""
    data = load_latest_json_data()
    articles = data.get('articles', [])
    metadata = data.get('metadata', {})

    # Get filter parameters
    filters = {
        'search': request.args.get('search', ''),
        'source': request.args.get('source', 'all'),
        'category': request.args.get('category', 'all')
    }

    # Apply filters
    filtered_articles = filter_articles(articles, filters)

    # Get unique sources and categories for dropdowns
    sources = list(set(article.get('source', 'Unknown') for article in articles))
    categories = list(set(article.get('category', 'Unknown') for article in articles))

    # Sort by date (newest first)
    filtered_articles.sort(key=lambda x: x.get('date', ''), reverse=True)

    return render_template('index.html',
                         articles=filtered_articles[:50],  # Limit to 50 articles
                         metadata=metadata,
                         sources=sorted(sources),
                         categories=sorted(categories),
                         filters=filters,
                         total_filtered=len(filtered_articles))

@app.route('/api/articles')
def api_articles():
    """API endpoint to get articles as JSON"""
    data = load_latest_json_data()
    articles = data.get('articles', [])

    # Get filter parameters
    filters = {
        'search': request.args.get('search', ''),
        'source': request.args.get('source', 'all'),
        'category': request.args.get('category', 'all')
    }

    # Apply filters
    filtered_articles = filter_articles(articles, filters)

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        'articles': filtered_articles[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': len(filtered_articles),
            'pages': (len(filtered_articles) + per_page - 1) // per_page
        }
    })

@app.route('/refresh')
def refresh_data():
    """Redirect to refresh data (would need to trigger scraping)"""
    # For now, just reload the page
    return "Data refresh functionality to be implemented"

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)

    print("Starting Indonesian News Viewer...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)