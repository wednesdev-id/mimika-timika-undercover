# 📰 Indonesian News Scraper & Web Viewer

A comprehensive Indonesian news scraper that collects articles from major news sources and displays them in a beautiful web interface.

## 🚀 Deployment Options

### Vercel Deployment (Demo Mode)

This project is configured for Vercel deployment with sample data:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod
```

**⚠️ Vercel Limitations**: Read-only demo with sample data. No scheduled scraping.

### Full Functionality Deployment

For complete scraping functionality, use:
- **[Railway.app](https://railway.app)** - Recommended for Python apps
- **[Render.com](https://render.com)** - Free tier available
- **[PythonAnywhere](https://www.pythonanywhere.com)** - Python hosting

## 🚀 Features

- **Multi-source Scraping**: Collects news from 6 major Indonesian news sites:
  - Kompas.com
  - CNN Indonesia
  - Antara News
  - Narasi
  - Tribun News
  - Detik.com

- **Real-time API Endpoints**:
  - ✅ Single-file API architecture (`api/index.py`)
  - ✅ Direct JSON response without file storage
  - ✅ Individual site scraping endpoints
  - ✅ Combined all-sites endpoint
  - ✅ CORS-enabled for frontend integration
  - ✅ Real-time scraping on-demand
  - ✅ 14 API endpoints in one file

- **Web Interface**: Beautiful, responsive web viewer with:
  - 🔍 Search functionality
  - 📂 Category filtering
  - 📡 Source filtering
  - 📊 Statistics dashboard
  - 📱 Mobile-responsive design

- **Advanced Features**:
  - ✅ Modular architecture - each site has its own scraper
  - ✅ Single-file API for easier deployment
  - ✅ Automatic duplicate removal based on URLs
  - ✅ Built-in scheduler for automated daily scraping
  - ✅ Comprehensive logging system
  - ✅ CLI interface for flexible usage
  - ✅ Random delays to respect server rate limits
  - ✅ Error handling and recovery
  - ✅ Serverless deployment ready (Vercel)
  - ✅ Simplified Vercel routing (single function)

## 📋 Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone/Download the project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create necessary directories:**
   ```bash
   mkdir -p data logs
   ```

4. **Create configuration file (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

## 📖 Usage

### 1. API Endpoints (Vercel Deployment)

**Real-time Scraping Endpoints:**
```bash
# Scrape all news sites
GET /api/scrape/all

# Scrape individual sites
GET /api/scrape/detik
GET /api/scrape/kompas
GET /api/scrape/cnn
GET /api/scrape/antara
GET /api/scrape/narasi
GET /api/scrape/tribun
```

**Data Access Endpoints:**
```bash
# Get main news data with filtering
GET /api?search=keyword&source=detik&category=news&page=1&per_page=20

# Get available sources
GET /api/sources

# Get available categories
GET /api/categories

# Get statistics
GET /api/stats

# API documentation
GET /docs          # Swagger UI
GET /redoc         # ReDoc
```

**API Response Format:**
```json
{
  "status": "success",
  "data": {
    "metadata": {
      "total_articles": 100,
      "last_updated": "2025-12-18T10:30:00",
      "sources": ["Detik.com", "Kompas.com"],
      "categories": ["news", "techno"]
    },
    "articles": [
      {
        "title": "Judul Berita",
        "url": "https://...",
        "description": "Deskripsi berita...",
        "date": "2025-12-18 10:00:00",
        "category": "news",
        "source": "Detik.com"
      }
    ]
  }
}
```

### 2. Local Scraping

**Scrape all sources (JSON output by default):**
```bash
python main.py
```

**Scrape specific site:**
```bash
python main.py --site detik
python main.py --site kompas
python main.py --site cnn
```

**Choose output format:**
```bash
python main.py --format json    # Default
python main.py --format csv
python main.py --format excel
```

**List available scrapers:**
```bash
python main.py --list
```

**Run with scheduler:**
```bash
python main.py --scheduler
```

### 3. Local Web Interface

**Start the web interface:**
```bash
python web_viewer.py
```

Then open your browser and go to: `http://localhost:5000`

### 4. Deployment

**Vercel Deployment:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to Vercel
vercel --prod

# Single function deployment - all routes handled by api/index.py
# Access endpoints at:
# https://your-app.vercel.app/api/scrape/all
# https://your-app.vercel.app/docs
# https://your-app.vercel.app/api/scrape/status
```

**Deployment Notes:**
- **Single Function**: All 14 endpoints served by one `api/index.py` function (803 lines)
- **Simplified Routing**: All requests (`/(.*)`) route to single function
- **Optimized Build**: Streamlined for serverless deployment
- **Reduced Cold Starts**: Single function architecture improves performance
- **Python 3.9**: Configured environment in `vercel.json`
- **CORS Enabled**: All endpoints support cross-origin requests

### 5. Environment Variables (Optional)

Create a `.env` file:

```env
# Output format: json, csv, excel
OUTPUT_FORMAT=json

# Scheduler settings
SCHEDULER_MODE=daily
SCHEDULER_TIME=08:00
SCHEDULER_INTERVAL=60
```

## 📊 Data Structure

### JSON Output Format
```json
{
  "metadata": {
    "total_articles": 150,
    "last_updated": "2025-11-04T10:30:00",
    "sources": ["Detik.com", "Kompas.com"],
    "categories": ["news", "hukum", "politik"]
  },
  "articles": [
    {
      "title": "Judul Berita",
      "url": "https://...",
      "description": "Deskripsi berita...",
      "date": "2025-11-04 10:00:00",
      "category": "news",
      "source": "Detik.com"
    }
  ]
}
```

## 📁 Project Structure

```
mimika_scraping/
├── main.py              # Main scraper script (local usage)
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config (single function)
├── .env.example        # Environment variables template
├── data/               # Local output files (CSV, JSON, Excel)
├── logs/               # Log files
├── api/                # Vercel serverless functions
│   └── index.py        # 🚀 ALL API ENDPOINTS (803 lines, 14 routes)
├── scrapers/           # Individual news site scrapers
│   ├── detik_scraper.py
│   ├── kompas_scraper.py
│   ├── cnn_scraper.py
│   ├── antara_scraper.py
│   ├── narasi_scraper.py
│   └── tribun_scraper.py
└── utils/              # Helper functions
    ├── helpers.py      # Data processing utilities
    └── scheduler.py    # Task scheduling (local)
```

**API Endpoints in `api/index.py`:**
- `GET /` - Main data endpoint
- `GET /api` - Filtered articles with pagination
- `GET /api/sources` - List available sources
- `GET /api/categories` - List available categories
- `GET /api/stats` - Statistics dashboard
- `GET /api/refresh` - Refresh information
- `GET /api/scrape/status` - API documentation
- `GET /api/scrape/all` - **Scrape all 6 news sites**
- `GET /api/scrape/detik` - **Scrape Detik.com**
- `GET /api/scrape/kompas` - **Scrape Kompas.com**
- `GET /api/scrape/cnn` - **Scrape CNN Indonesia**
- `GET /api/scrape/antara` - **Scrape Antara News**
- `GET /api/scrape/narasi` - **Scrape Narasi**
- `GET /api/scrape/tribun` - **Scrape Tribun News**
- `GET /health` - Health check

## 🎯 Web Interface Features

- **Search**: Search articles by title and description
- **Filtering**: Filter by news source and category
- **Statistics**: View total articles, sources, and last update time
- **Responsive**: Works on desktop and mobile devices
- **Real-time**: Auto-refresh option every 5 minutes
- **External Links**: Click to read full articles on source websites

## Data Format

Each scraped article contains the following fields:

| Field | Description |
|-------|-------------|
| title | Article title |
| date | Publication date (YYYY-MM-DD HH:MM:SS) |
| url | Article URL |
| description | Article description/excerpt |
| category | News category/topic |
| source | Source website name |

## Configuration

Create a `.env` file in the project root to customize behavior:

```env
# Output format: csv or excel
OUTPUT_FORMAT=csv

# Scheduler settings
SCHEDULER_MODE=daily
SCHEDULER_TIME=08:00
SCHEDULER_INTERVAL=60

# Optional: Custom data path
DATA_PATH=./data
```

## Scheduling

### Daily Scheduling
The scheduler can automatically run scraping at specified times:

```bash
# Schedule daily at 8:00 AM
python utils/scheduler.py --mode daily --time 08:00

# Schedule daily at 6:00 PM
python utils/scheduler.py --mode daily --time 18:00
```

### Interval Scheduling
Run scraping at regular intervals:

```bash
# Run every 30 minutes
python utils/scheduler.py --mode interval --interval 30

# Run every 2 hours
python utils/scheduler.py --mode interval --interval 120
```

## Individual Scraper Testing

Test each scraper individually:

```bash
# Test Kompas scraper
python scrapers/kompas_scraper.py

# Test CNN scraper
python scrapers/cnn_scraper.py

# Test Antara scraper
python scrapers/antara_scraper.py

# Test Narasi scraper
python scrapers/narasi_scraper.py

# Test Tribun scraper
python scrapers/tribun_scraper.py

# Test Detik scraper
python scrapers/detik_scraper.py
```

## Logging

All scraping activities are logged to `logs/scrape_log.txt` and also displayed in the console. Log levels include:
- INFO: Successful operations
- WARNING: Non-critical issues
- ERROR: Critical errors

## Output Files

- CSV files: `data/news_YYYYMMDD.csv`
- Excel files: `data/news_YYYYMMDD.xlsx`
- Site-specific files: `data/news_sitename_YYYYMMDD.csv/xlsx`

## Error Handling

The application includes robust error handling:
- Network timeouts and connection errors
- Website structure changes
- Missing or malformed data
- Rate limiting protection

## 🔧 API Integration Examples

### JavaScript/Frontend Integration
```javascript
// Fetch latest news from all sources
async function fetchLatestNews() {
  try {
    const response = await fetch('https://your-app.vercel.app/api/scrape/all');
    const data = await response.json();

    if (data.status === 'success') {
      console.log(`Found ${data.data.metadata.total_articles} articles`);
      return data.data.articles;
    }
  } catch (error) {
    console.error('Error fetching news:', error);
  }
}

// Fetch from specific source
async function fetchDetikNews() {
  const response = await fetch('https://your-app.vercel.app/api/scrape/detik');
  return await response.json();
}
```

### Python Integration
```python
import requests

# Fetch from all sources
response = requests.get('https://your-app.vercel.app/api/scrape/all')
data = response.json()

if data['status'] == 'success':
    articles = data['data']['articles']
    print(f"Total articles: {len(articles)}")
```

### cURL Examples
```bash
# Scrape all sites
curl https://your-app.vercel.app/api/scrape/all

# Scrape specific site
curl https://your-app.vercel.app/api/scrape/detik

# Get API documentation
curl https://your-app.vercel.app/api/scrape/status
```

## Contributing

1. Fork the repository
2. Create a new scraper in the `scrapers/` directory
3. Add the scraper to `api/index.py` following the existing pattern:
   - Implement a `scrape_<sitename>()` function in the scraper file
   - Add the scraper import in the API endpoints section
   - Add the scraper to the `SCRAPERS` dictionary in `/api/scrape/all` endpoint
   - Create a new endpoint `@app.get("/api/scrape/<sitename>")` following the pattern
4. Test thoroughly
5. Submit a pull request

**Example for Adding New Scraper:**
```python
# In api/index.py - add import
from scrapers.newsite_scraper import scrape_newsite

# In scrape_all_sites function - add to SCRAPERS dict
SCRAPERS = {
    'kompas': scrape_kompas,
    'cnn': scrape_cnn,
    'antara': scrape_antara,
    'narasi': scrape_narasi,
    'tribun': scrape_tribun,
    'detik': scrape_detik,
    'newsite': scrape_newsite  # Add new scraper
}

# Add new endpoint
@app.get("/api/scrape/newsite")
async def scrape_newsite_endpoint():
    """Scrape NewSite and return JSON response"""
    # Follow existing pattern...
```

## Best Practices

- ⚠️ Respect website robots.txt files
- ⚠️ Use appropriate delays between requests
- ⚠️ Don't overload servers
- ⚠️ Consider fair use policies
- ⚠️ Monitor logs regularly
- 🚀 For production use, implement caching and rate limiting
- 🌐 Consider Vercel function timeouts (max 10 seconds for hobby tier)

## Troubleshooting

### Common Issues

1. **No articles scraped**: Check if website structure has changed
2. **Connection timeouts**: Increase timeout values or check internet connection
3. **Rate limiting**: Increase delay values between requests
4. **Missing dependencies**: Run `pip install -r requirements.txt`
5. **Vercel function timeout**: Scraping may take longer than Vercel's timeout limits
6. **CORS errors**: Ensure proper CORS headers in API responses

### Debug Mode

Enable debug logging by modifying `utils/helpers.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

For production deployment on Vercel:
- **Single-file architecture**: All endpoints in one function reduces cold starts
- **Function timeout awareness**: Monitor execution times (Vercel hobby tier: 10s, pro: 60s)
- **Caching strategy**: Implement with external services (Redis, Upstash) for repeated requests
- **Rate limiting**: Consider server limits and implement request throttling
- **Error handling**: Built-in retry mechanisms for failed scrapes
- **Monitoring**: Use Vercel Analytics to track function performance

**Deployment Tips:**
```bash
# Check function size and performance
vercel logs

# Monitor specific endpoints
curl -w "@curl-format.txt" https://your-app.vercel.app/api/scrape/detik

# Use environment variables for production
vercel env add SECRET_KEY
```

**Optimization Notes:**
- Individual scrapers are faster than `/api/scrape/all` for single-source requests
- Consider running scrapers in parallel for multiple sources
- Large scraping jobs may need to be split across multiple functions
- Memory usage increases with article count - monitor Vercel function limits

## License

This project is for educational and research purposes. Users are responsible for complying with the terms of service of the target websites.

## Disclaimer

This tool should be used responsibly and in accordance with the terms of service of the target websites. The authors are not responsible for any misuse of this software.