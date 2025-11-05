# Papua News - Indonesian News Scraper Project

## Project Overview
Papua News is a comprehensive Indonesian news scraping system that collects, processes, and displays news articles from major Indonesian news sources. The project provides both automated scraping capabilities and a web interface for viewing and searching news content.

## Architecture

### Components
1. **Scrapers** (`scrapers/`) - Individual scrapers for each news source
2. **Utilities** (`utils/`) - Helper functions and scheduling system
3. **Web API** (`web_api.py`) - FastAPI-based web interface and REST API
4. **Main Application** (`main.py`) - CLI interface for running scrapers
5. **Data Storage** (`data/`) - JSON files containing scraped articles

### Supported News Sources
- **Kompas** - kompas.com
- **CNN Indonesia** - cnnindonesia.com
- **Antara News** - antaranews.com
- **Detik** - detik.com
- **Tribun** - tribunnews.com
- **Narasi** - narasi.tv

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Papua News"
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create necessary directories**
   ```bash
   mkdir -p data templates static
   ```

5. **Run the application**
   ```bash
   # Start the web API
   python web_api.py

   # Or run scraping manually
   python main.py
   ```

## Usage

### Web Interface
1. Start the FastAPI server:
   ```bash
   python web_api.py
   ```
2. Open browser to: `http://localhost:8000`
3. Use the web interface to:
   - Browse news articles
   - Search by keywords
   - Filter by source and category
   - View statistics

### Command Line Interface

#### Scrape all sources
```bash
python main.py
```

#### Scrape specific source
```bash
python main.py --site kompas
python main.py --site cnn
python main.py --site antara
```

#### Specify output format
```bash
python main.py --format json    # Default
python main.py --format csv
python main.py --format excel
```

#### Run scheduler
```bash
python main.py --scheduler
```

#### List available scrapers
```bash
python main.py --list
```

### API Endpoints

#### Main Articles API
```bash
# Get all articles
curl "http://localhost:8000/api"

# Search with filters
curl "http://localhost:8000/api?search=politik&source=kompas&page=1"

# Get all articles without pagination
curl "http://localhost:8000/api?all=true"
```

#### Utility Endpoints
```bash
# Get sources
curl "http://localhost:8000/api/sources"

# Get categories
curl "http://localhost:8000/api/categories"

# Get statistics
curl "http://localhost:8000/api/stats"

# Health check
curl "http://localhost:8000/health"
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Output format for scraped data
OUTPUT_FORMAT=json

# Scheduler configuration
SCHEDULER_MODE=daily
SCHEDULER_TIME=08:00
SCHEDULER_INTERVAL=60

# Web API configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
```

### Scheduler Configuration

#### Daily Mode
```env
SCHEDULER_MODE=daily
SCHEDULER_TIME=08:00
```

#### Hourly Mode
```env
SCHEDULER_MODE=hourly
```

#### Interval Mode
```env
SCHEDULER_MODE=interval
SCHEDULER_INTERVAL=30  # minutes
```

## Data Structure

### Article Object
```json
{
  "title": "Article Title",
  "description": "Article description or summary",
  "url": "https://news-source.com/article-url",
  "source": "source-name",
  "category": "article-category",
  "date": "2024-01-01T12:00:00Z"
}
```

### Data Files
- **Location**: `data/` directory
- **Format**: JSON files
- **Naming**: `news_YYYYMMDD.json`
- **Structure**:
```json
{
  "metadata": {
    "total_articles": 150,
    "last_updated": "2024-01-01T12:00:00Z",
    "sources": ["kompas", "cnn", "antara"],
    "scraping_duration": "2.5 minutes"
  },
  "articles": [
    {
      "title": "Article Title",
      "description": "Description",
      "url": "https://...",
      "source": "kompas",
      "category": "politik",
      "date": "2024-01-01"
    }
  ]
}
```

## Development

### Project Structure

```
Papua News/
├── api/                    # Vercel serverless functions
│   └── index.py           # FastAPI app for Vercel deployment
├── scrapers/              # Individual news source scrapers
│   ├── kompas_scraper.py
│   ├── cnn_scraper.py
│   ├── antara_scraper.py
│   ├── detik_scraper.py
│   ├── tribun_scraper.py
│   └── narasi_scraper.py
├── utils/                 # Utility functions
│   ├── helpers.py
│   └── scheduler.py
├── docs/                  # Documentation files
│   ├── API_DOCUMENTATION.md
│   ├── FRONTEND_INTEGRATION.md
│   └── PROJECT_DOCUMENTATION.md
├── data/                  # Scraped data storage
├── templates/             # HTML templates
├── static/                # Static files (CSS, JS, images)
├── logs/                  # Log files
├── main.py               # CLI application
├── web_api.py            # FastAPI web server (local)
├── vercel.json           # Vercel configuration
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

### File Explanations

#### Core Files
- **`main.py`**: CLI interface for running scrapers
- **`web_api.py`**: FastAPI application for local development
- **`api/index.py`**: Serverless version for Vercel deployment
- **`vercel.json`**: Vercel deployment configuration

#### Data Directories
- **`data/`**: JSON files with scraped news data
- **`templates/`**: HTML templates for web interface
- **`static/`**: CSS, JavaScript, and image assets
- **`logs/`**: Application logs

#### Configuration
- **`requirements.txt`**: Python dependencies
- **`.env.example`**: Environment variables template
- **`docs/`**: Comprehensive documentation

### Adding New Scrapers

1. **Create scraper file** in `scrapers/` directory:
   ```python
   # scrapers/newsource_scraper.py
   import pandas as pd
   from bs4 import BeautifulSoup
   import requests

   def scrape_newsource():
       """Scrape articles from newsource.com"""
       articles = []

       # Your scraping logic here
       # Return pandas DataFrame with columns:
       # ['title', 'description', 'url', 'source', 'category', 'date']

       return pd.DataFrame(articles)
   ```

2. **Update main.py** to include new scraper:
   ```python
   # Import the new scraper
   from scrapers.newsource_scraper import scrape_newsource

   # Add to SCRAPERS dictionary
   SCRAPERS = {
       'kompas': scrape_kompas,
       'cnn': scrape_cnn,
       'newsource': scrape_newsource  # Add this line
   }
   ```

3. **Test the scraper**:
   ```bash
   python main.py --site newsource
   ```

### Testing

#### Run all scrapers
```bash
python test_scrape.py
```

#### Test individual scraper
```python
from scrapers.kompas_scraper import scrape_kompas
df = scrape_kompas()
print(f"Scraped {len(df)} articles")
```

## Deployment

### Option 1: Vercel (Demo Mode - Recommended for Quick Preview)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod
```

**Best for**: Quick demos, frontend showcase, read-only API
**Limitations**:
- Sample data only (no real scraping)
- No scheduled tasks
- Serverless file system restrictions

### Option 2: Railway (Recommended for Full Functionality)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Best for**: Full scraping functionality, scheduled tasks, production use
**Features**:
- Complete scraping capabilities
- Scheduled data updates
- Persistent storage
- Database support

### Option 3: Render (Free Tier Available)

1. Connect your GitHub repository to [Render](https://render.com)
2. Create a new "Web Service"
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn web_api:app --host 0.0.0.0 --port $PORT`
   - Python Version: 3.9 or higher

### Option 4: PythonAnywhere

1. Create a PythonAnywhere account
2. Upload your project files
3. Configure virtual environment
4. Install dependencies
5. Set up web app with Flask/FastAPI
6. Configure scheduled tasks for scraping

### Development
```bash
# Local development
python web_api.py

# Or for Vercel testing
python api/index.py
```

### Production (using Gunicorn)
```bash
pip install gunicorn
gunicorn web_api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "web_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  news-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - API_DEBUG=false
    restart: unless-stopped

  scheduler:
    build: .
    command: python main.py --scheduler
    volumes:
      - ./data:/app/data
    environment:
      - SCHEDULER_MODE=daily
      - SCHEDULER_TIME=08:00
    restart: unless-stopped
```

## Vercel Configuration Details

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  }
}
```

### Vercel Environment Variables
- `VERCEL_ENV`: `production`
- `PYTHON_VERSION`: `3.9`
- `API_BASE_URL`: Your Vercel deployment URL

## Railway Configuration Details

### railway.toml
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn web_api:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10

[[services]]
name = "api"

[services.variables]
PYTHON_VERSION = "3.9"
```

### Railway Environment Variables
- `RAILWAY_ENVIRONMENT`: `production`
- `API_HOST`: `0.0.0.0`
- `API_PORT`: `$PORT` (Railway provides this)
- `SCHEDULER_MODE`: `daily`
- `SCHEDULER_TIME`: `08:00`

## Monitoring & Maintenance

### Log Files
- **Scraping logs**: Stored in `logs/` directory
- **Web server logs**: Console output (configure as needed)

### Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Check data freshness
curl http://localhost:8000/api/stats | jq '.latest_date'
```

### Data Cleanup
```python
# Clean old data files (keep last 30 days)
import os
from datetime import datetime, timedelta

def cleanup_old_data():
    data_dir = 'data'
    cutoff_date = datetime.now() - timedelta(days=30)

    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            file_date = datetime.strptime(filename.split('_')[1].split('.')[0], '%Y%m%d')
            if file_date < cutoff_date:
                os.remove(os.path.join(data_dir, filename))
                print(f"Removed old file: {filename}")
```

## API Rate Limiting & Best Practices

### Current Limitations
- No built-in rate limiting
- No authentication system
- No request caching

### Recommendations for Production
1. **Implement API keys**
2. **Add rate limiting** (using slowapi or similar)
3. **Add caching** (Redis)
4. **Set up monitoring** (Prometheus/Grafana)
5. **Configure backups** for data directory
6. **Implement logging** and log rotation

## Troubleshooting

### Common Issues

#### Scraping Fails
- Check internet connection
- Verify news source website is accessible
- Check if website structure has changed
- Review scraper-specific error messages

#### API Not Starting
- Verify port 8000 is not in use
- Check if all dependencies are installed
- Review error messages in console

#### Data Not Loading
- Verify `data/` directory exists
- Check if JSON files are valid
- Ensure file permissions are correct

#### Performance Issues
- Check server resources (CPU, memory)
- Monitor response times
- Consider implementing caching

### Getting Help
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Test individual components separately
4. Check network connectivity
5. Review this documentation

## Contributing

### Guidelines
1. Follow PEP 8 coding standards
2. Add proper error handling
3. Include docstrings for new functions
4. Test your changes thoroughly
5. Update documentation as needed

### Pull Request Process
1. Fork the repository
2. Create feature branch
3. Make your changes
4. Add tests if applicable
5. Submit pull request with description

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Changelog

### Version 2.0.0 (Current)
- **Vercel Support**: Added serverless deployment configuration
- **Multi-Platform Deployment**: Vercel, Railway, Render, PythonAnywhere support
- **FastAPI Migration**: Migrated from Flask to FastAPI
- **Unified API endpoints**: RESTful API with pagination
- **Comprehensive Documentation**: API docs, frontend integration guide, project docs
- **Sample Data**: Demo data for Vercel deployment
- **Optimized Dependencies**: Serverless-friendly requirements
- **Better error handling**: Improved error responses and logging
- **Enhanced security**: CORS, environment variables
- **Project structure reorganization**: Separate API for serverless

### Version 1.0.0
- Initial release
- Basic scraping functionality
- Flask web interface
- Command line tools

## Next Steps & Future Improvements

### Immediate Tasks
- [ ] Deploy to Vercel for demo
- [ ] Set up Railway for full functionality
- [ ] Configure scheduled scraping
- [ ] Add API authentication for production

### Future Features
- **Database Integration**: PostgreSQL/MongoDB for better data management
- **Caching Layer**: Redis for performance optimization
- **API Rate Limiting**: Prevent abuse and ensure fair usage
- **User Authentication**: Personalized news feeds and preferences
- **Mobile App**: React Native or Flutter app
- **Analytics Dashboard**: News trend analysis
- **Email Notifications**: Daily/weekly news summaries
- **RSS Feeds**: Generate RSS feeds for categories
- **Advanced Search**: Full-text search with indexing
- **Social Media Integration**: Share articles to social platforms