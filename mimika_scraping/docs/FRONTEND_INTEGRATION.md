# Frontend Integration Guide

## Overview
This guide explains how to integrate with the Indonesian News API for frontend applications. The API provides both a ready-to-use web interface and RESTful endpoints for custom frontend implementations.

## Quick Start Options

### Option 1: Use Built-in Web Interface
The API includes a responsive web interface at the root URL:

**Local Development**:
```
http://localhost:8000
```

**Vercel Deployment**:
```
https://your-app-name.vercel.app
```

**Other Deployments**:
- Railway: `https://your-app-name.up.railway.app`
- Render: `https://your-app-name.onrender.com`

Features:
- ✅ Responsive design for mobile and desktop
- ✅ Real-time search and filtering
- ✅ Beautiful UI with modern design
- ✅ Automatic refresh notifications
- ✅ Source and category filtering

### Option 2: Build Custom Frontend
Use the REST API endpoints to build your own frontend application.

## API Integration Examples

### 1. JavaScript/TypeScript Integration

#### Basic Fetch Example
```javascript
// Configure API base URL based on environment
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://your-app-name.vercel.app'  // Replace with your Vercel URL
  : 'http://localhost:8000';

// Get all articles with pagination
async function getArticles(page = 1, perPage = 20) {
  try {
    const response = await fetch(`${API_BASE_URL}/api?page=${page}&per_page=${perPage}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching articles:', error);
    throw error;
  }
}

// Get articles with filters
async function getFilteredArticles(search, source, category) {
  const params = new URLSearchParams({
    search: search || '',
    source: source || 'all',
    category: category || 'all'
  });

  const response = await fetch(`/api?${params}`);
  return await response.json();
}

// Usage examples
const allArticles = await getArticles();
const filteredArticles = await getFilteredArticles('politik', 'kompas', 'politik');
```

#### React Component Example
```jsx
import React, { useState, useEffect } from 'react';

function NewsViewer() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    search: '',
    source: 'all',
    category: 'all'
  });
  const [pagination, setPagination] = useState(null);

  useEffect(() => {
    fetchArticles();
  }, [filters]);

  const fetchArticles = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams(filters);
      const response = await fetch(`/api?${params}`);
      const data = await response.json();
      setArticles(data.articles);
      setPagination(data.pagination);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (event) => {
    setFilters({...filters, search: event.target.value});
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <input
        type="text"
        placeholder="Search articles..."
        onChange={handleSearch}
        value={filters.search}
      />

      <div className="articles">
        {articles.map(article => (
          <div key={article.url} className="article-card">
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <div className="meta">
              <span className="source">{article.source}</span>
              <span className="category">{article.category}</span>
              <span className="date">{article.date}</span>
            </div>
            <a href={article.url} target="_blank" rel="noopener noreferrer">
              Read more
            </a>
          </div>
        ))}
      </div>

      {pagination && (
        <div className="pagination">
          <button
            onClick={() => fetchArticles(pagination.page - 1)}
            disabled={pagination.page === 1}
          >
            Previous
          </button>
          <span>Page {pagination.page} of {pagination.pages}</span>
          <button
            onClick={() => fetchArticles(pagination.page + 1)}
            disabled={pagination.page === pagination.pages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default NewsViewer;
```

#### Vue.js Component Example
```vue
<template>
  <div class="news-viewer">
    <div class="filters">
      <input
        v-model="filters.search"
        @input="fetchArticles"
        placeholder="Search articles..."
      />
      <select v-model="filters.source" @change="fetchArticles">
        <option value="all">All Sources</option>
        <option v-for="source in sources" :key="source" :value="source">
          {{ source }}
        </option>
      </select>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else class="articles">
      <article
        v-for="article in articles"
        :key="article.url"
        class="article-card"
      >
        <h3>{{ article.title }}</h3>
        <p>{{ article.description }}</p>
        <div class="meta">
          <span class="source">{{ article.source }}</span>
          <span class="category">{{ article.category }}</span>
          <span class="date">{{ formatDate(article.date) }}</span>
        </div>
        <a :href="article.url" target="_blank">Read more</a>
      </article>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'NewsViewer',
  setup() {
    const articles = ref([]);
    const sources = ref([]);
    const loading = ref(true);
    const filters = ref({
      search: '',
      source: 'all',
      category: 'all'
    });

    const fetchArticles = async () => {
      loading.value = true;
      try {
        const params = new URLSearchParams(filters.value);
        const response = await fetch(`/api?${params}`);
        const data = await response.json();
        articles.value = data.articles;
      } catch (error) {
        console.error('Error fetching articles:', error);
      } finally {
        loading.value = false;
      }
    };

    const fetchSources = async () => {
      try {
        const response = await fetch('/api/sources');
        const data = await response.json();
        sources.value = data.sources;
      } catch (error) {
        console.error('Error fetching sources:', error);
      }
    };

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString();
    };

    onMounted(async () => {
      await fetchSources();
      await fetchArticles();
    });

    return {
      articles,
      sources,
      loading,
      filters,
      fetchArticles,
      formatDate
    };
  }
};
</script>
```

### 2. Python Integration

#### Using requests library
```python
import requests
from typing import List, Dict, Optional
import os

class NewsAPIClient:
    def __init__(self, base_url: str = None):
        # Auto-detect base URL based on environment
        if base_url is None:
            if os.getenv('VERCEL_ENV') or os.getenv('RAILWAY_ENVIRONMENT'):
                base_url = os.getenv('API_BASE_URL', 'https://your-app-name.vercel.app')
            else:
                base_url = 'http://localhost:8000'
        self.base_url = base_url

    def get_articles(
        self,
        search: Optional[str] = None,
        source: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
        all_articles: bool = False
    ) -> Dict:
        """Get articles with optional filters"""
        params = {
            'page': page,
            'per_page': per_page,
            'all': all_articles
        }

        if search:
            params['search'] = search
        if source:
            params['source'] = source
        if category:
            params['category'] = category

        response = requests.get(f"{self.base_url}/api", params=params)
        response.raise_for_status()
        return response.json()

    def get_sources(self) -> Dict:
        """Get available news sources"""
        response = requests.get(f"{self.base_url}/api/sources")
        response.raise_for_status()
        return response.json()

    def get_categories(self) -> Dict:
        """Get available categories"""
        response = requests.get(f"{self.base_url}/api/categories")
        response.raise_for_status()
        return response.json()

    def get_stats(self) -> Dict:
        """Get statistics about the news data"""
        response = requests.get(f"{self.base_url}/api/stats")
        response.raise_for_status()
        return response.json()

# Usage example
client = NewsAPIClient()

# Get all articles
articles = client.get_articles()

# Search for specific articles
politics_articles = client.get_articles(search="politik", source="kompas")

# Get statistics
stats = client.get_stats()
print(f"Total articles: {stats['total_articles']}")
```

### 3. Other Languages Examples

#### cURL Examples
```bash
# Local development
API_BASE="http://localhost:8000"

# Vercel deployment
API_BASE="https://your-app-name.vercel.app"

# Get all articles
curl "$API_BASE/api"

# Search with filters
curl "$API_BASE/api?search=politik&source=kompas&page=1&per_page=10"

# Get sources
curl "$API_BASE/api/sources"

# Get statistics
curl "$API_BASE/api/stats"
```

#### PHP Example
```php
<?php
class NewsAPIClient {
    private $baseUrl;

    public function __construct($baseUrl = "http://localhost:8000") {
        $this->baseUrl = $baseUrl;
    }

    public function getArticles($params = []) {
        $url = $this->baseUrl . "/api?" . http_build_query($params);
        $response = file_get_contents($url);
        return json_decode($response, true);
    }

    public function getSources() {
        $response = file_get_contents($this->baseUrl . "/api/sources");
        return json_decode($response, true);
    }
}

// Usage
$client = new NewsAPIClient();
$articles = $client->getArticles(['search' => 'politik', 'page' => 1]);
$sources = $client->getSources();
?>
```

## Styling Examples

### CSS for Article Cards
```css
.articles-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.article-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-left: 4px solid #3498db;
  transition: transform 0.2s, box-shadow 0.2s;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.article-title {
  color: #2c3e50;
  font-size: 1.3em;
  margin-bottom: 10px;
  line-height: 1.4;
}

.article-description {
  color: #495057;
  line-height: 1.6;
  margin-bottom: 15px;
}

.article-meta {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.source-tag, .category-tag {
  background: #f1f3f4;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: 500;
}

.source-tag {
  background: #e3f2fd;
  color: #1976d2;
}

.category-tag {
  background: #f3e5f5;
  color: #7b1fa2;
}

.article-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.article-link:hover {
  text-decoration: underline;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #6c757d;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.pagination button {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

.pagination button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
```

## Deployment Considerations

### CORS Configuration
If your frontend is hosted on a different domain, ensure CORS is properly configured:

```python
# In web_api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables
Configure these for production:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=false

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Caching (if implemented)
REDIS_URL=redis://localhost:6379
```

### Security Best Practices
1. **API Keys**: Implement API key authentication for production
2. **Rate Limiting**: Add rate limiting to prevent abuse
3. **HTTPS**: Use HTTPS in production
4. **Input Validation**: Always validate and sanitize inputs
5. **Content Security Policy**: Implement CSP headers

## Performance Optimization

### Client-Side
```javascript
// Implement client-side caching
const cache = new Map();

async function getCachedArticles(params) {
  const cacheKey = JSON.stringify(params);

  if (cache.has(cacheKey)) {
    return cache.get(cacheKey);
  }

  const articles = await fetchArticles(params);
  cache.set(cacheKey, articles);

  // Clear cache after 5 minutes
  setTimeout(() => cache.delete(cacheKey), 300000);

  return articles;
}

// Implement infinite scroll
let currentPage = 1;
let loading = false;

async function loadMoreArticles() {
  if (loading) return;

  loading = true;
  const newArticles = await getArticles(currentPage + 1);

  // Append to existing articles
  appendArticles(newArticles.articles);
  currentPage++;
  loading = false;
}

// Debounce search input
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

const debouncedSearch = debounce((searchTerm) => {
  fetchArticles({ search: searchTerm });
}, 300);
```

## Deployment Considerations for Frontend

### Vercel Deployment (Recommended for Frontend)
If you're building a custom frontend (React, Vue, Angular), Vercel is excellent for hosting:

```json
// vercel.json for frontend app
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### Environment Configuration
```javascript
// config/api.js
const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8000'
  },
  production: {
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'https://your-app-name.vercel.app'
  }
};

export const API_BASE_URL = API_CONFIG[process.env.NODE_ENV] || API_CONFIG.development;
```

### CORS Configuration
If deploying frontend separately from API, configure CORS in the API:

```python
# In web_api.py or api/index.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://your-frontend.vercel.app",  # Your frontend domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables for Deployment
```bash
# For Vercel frontend
NEXT_PUBLIC_API_URL=https://your-api.vercel.app

# For Railway backend
RAILWAY_ENVIRONMENT=production
API_BASE_URL=https://your-api.up.railway.app
```

This integration guide provides comprehensive examples for building custom frontend applications that consume the Indonesian News API. Choose the option that best fits your project requirements.