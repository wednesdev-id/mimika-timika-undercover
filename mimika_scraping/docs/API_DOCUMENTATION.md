# Indonesian News API Documentation

## Overview
Indonesian News API is a FastAPI-based web service that provides access to scraped Indonesian news data from multiple sources. It offers both a web interface and RESTful API endpoints for consuming news data.

## Base URLs

### Local Development
```
http://localhost:8000
```

### Vercel Deployment (Demo Mode)
```
https://your-app-name.vercel.app
```

### Full Deployment Options
- **Railway.app**: `https://your-app-name.up.railway.app`
- **Render.com**: `https://your-app-name.onrender.com`
- **PythonAnywhere**: `https://your-username.pythonanywhere.com`

**Note**: Vercel deployment provides read-only demo with sample data. For full scraping functionality, use Railway, Render, or PythonAnywhere.

## Available Endpoints

### 1. Main Web Interface
```
GET /
```
- **Description**: Main HTML page with news display and filtering
- **Response**: HTML page with news articles
- **Query Parameters**:
  - `search` (string): Search keywords in title or description
  - `source` (string): Filter by news source (default: "all")
  - `category` (string): Filter by category (default: "all")

### 2. Get Articles (Main API Endpoint)
```
GET /api
```
- **Description**: Retrieve articles with filtering and pagination
- **Response**: JSON with articles and pagination info
- **Query Parameters**:
  - `search` (string, optional): Search keywords in title or description
  - `source` (string, optional): Filter by news source (default: "all")
  - `category` (string, optional): Filter by category (default: "all")
  - `page` (integer, optional): Page number for pagination (default: 1)
  - `per_page` (integer, optional): Items per page (default: 20, max: 100)
  - `all` (boolean, optional): Return all articles without pagination (default: false)

**Response Model**:
```json
{
  "articles": [
    {
      "title": "Article Title",
      "description": "Article description",
      "url": "https://example.com/article",
      "source": "news-source",
      "category": "category-name",
      "date": "2024-01-01"
    }
  ],
  "total": 150,
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

### 3. Get News Sources
```
GET /api/sources
```
- **Description**: Get list of all available news sources
- **Response**: JSON with sources list

**Response Model**:
```json
{
  "sources": ["kompas", "cnn", "antara", "detik", "tribun", "narasi"],
  "total": 6
}
```

### 4. Get Categories
```
GET /api/categories
```
- **Description**: Get list of all available categories
- **Response**: JSON with categories list

**Response Model**:
```json
{
  "categories": ["politik", "ekonomi", "olahraga", "teknologi", "hiburan"],
  "total": 5
}
```

### 5. Get Statistics
```
GET /api/stats
```
- **Description**: Get comprehensive statistics about the news data
- **Response**: JSON with detailed statistics

**Response Model**:
```json
{
  "metadata": {
    "total_articles": 500,
    "last_updated": "2024-01-01T12:00:00Z",
    "sources": ["kompas", "cnn"],
    "scraping_duration": "2.5 minutes"
  },
  "total_articles": 500,
  "total_sources": 6,
  "total_categories": 8,
  "sources": ["kompas", "cnn", "antara"],
  "categories": ["politik", "ekonomi", "olahraga"],
  "source_distribution": {
    "kompas": 100,
    "cnn": 85,
    "antara": 75
  },
  "category_distribution": {
    "politik": 120,
    "ekonomi": 100,
    "olahraga": 80
  },
  "latest_date": "2024-01-01"
}
```

### 6. Refresh Data
```
GET /api/refresh
```
- **Description**: Trigger data refresh (placeholder for future implementation)
- **Response**: JSON with refresh status

### 7. Health Check
```
GET /health
```
- **Description**: API health check endpoint
- **Response**: JSON with health status

**Response Model**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "2.0.0"
}
```

## Interactive Documentation

### Local Development
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Vercel Deployment
- **Swagger UI**: `https://your-app-name.vercel.app/docs`
- **ReDoc**: `https://your-app-name.vercel.app/redoc`

### Other Deployments
Replace the domain accordingly for Railway, Render, or PythonAnywhere deployments.

## Data Model

### Article Structure
Each article object contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Article title |
| `description` | string | Article description/content summary |
| `url` | string | URL to the original article |
| `source` | string | News source name (e.g., "kompas", "cnn") |
| `category` | string | Article category (e.g., "politik", "ekonomi") |
| `date` | string | Publication date (ISO format) |

## Error Handling
The API returns standard HTTP status codes:

- `200 OK`: Successful request
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses follow this format:
```json
{
  "detail": "Error message description"
}
```

## Rate Limiting
Currently, there are no rate limits implemented, but it's recommended to implement them for production use.

## Caching
- Data is loaded from the latest JSON file in the `data/` directory
- No server-side caching is implemented (data is refreshed on each request)
- Consider implementing Redis caching for production use

## Security Considerations
- API is currently open without authentication
- Consider implementing API keys for production use
- Input validation is implemented for query parameters
- CORS is enabled by default in FastAPI

## Running the API

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server
python web_api.py
```

### Production
```bash
# Using uvicorn directly
uvicorn web_api:app --host 0.0.0.0 --port 8000 --workers 4

# Using gunicorn (recommended for production)
pip install gunicorn
gunicorn web_api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Environment Variables
No specific environment variables are required for the API itself, but the scraper uses:
- `OUTPUT_FORMAT`: Output format for scraped data (json, csv, excel)
- `SCHEDULER_MODE`: Scheduler mode (daily, hourly, interval)
- `SCHEDULER_TIME`: Time for daily scheduling (HH:MM format)
- `SCHEDULER_INTERVAL`: Interval in minutes for interval scheduling

## Data Storage

### Local & Full Deployment
- Articles are stored in JSON files in the `data/` directory
- File naming convention: `news_YYYYMMDD.json`
- The API automatically loads the latest file based on filename sorting

### Vercel Deployment
- **Read-only demo mode** with sample data
- No persistent file storage (serverless limitation)
- Sample data embedded in the application for demonstration

## Deployment Options

### Vercel (Demo Mode)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Limitations**:
- Read-only with sample data
- No scheduled scraping
- Serverless file system restrictions

### Railway (Recommended for Full Functionality)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Render (Free Tier Available)
1. Connect your GitHub repository
2. Configure Python environment
3. Deploy with web service

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "8000"]
```