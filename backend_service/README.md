# 📰 Indonesian News Scraper & Web Viewer

A comprehensive Indonesian news scraper with **integrated flow architecture** that collects articles from major news sources using centralized main.py logic for both CLI and API interfaces.

## 🚀 Key Features

- **🔄 Integrated Flow Architecture**: Single source of truth in `main.py` serving both CLI and API
- **📡 Real-time API Endpoints**: Comprehensive endpoints with direct JSON response (no file storage)
- **💻 CLI Interface**: Traditional file-based scraping with multiple output formats
- **🌐 Single-File API**: Integrated endpoints in `api/index.py`
- **🔧 Modular Scrapers**: 6+ individual news site scrapers with centralized logic
- **🎯 Keyword Focused**: Optimized for "mimika timika" search across all major sources
- **🚀 Production Ready**: Optimized for Vercel serverless deployment
- **📢 Enhanced Logging**: New source-prefixed logs for better tracking

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

- **Multi-source Scraping**: Collects news from 6 major Indonesian news sites (expandable):
  - Kompas.com
  - Detik.com
  - CNN Indonesia
  - Antara News
  - Tempo
  - Kumparan
  - *Planned: Tribun News*

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
GET /api/scrape/tempo
GET /api/scrape/kumparan
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

# Integrated architecture deployment:
# - Single function: api/index.py (472 lines, 14 endpoints)
# - Centralized scraping: main.py shared between CLI and API
# - All routes handled by api/index.py with main.py integration
# Access endpoints at:
# https://your-app.vercel.app/api/scrape/all
# https://your-app.vercel.app/docs
# https://your-app.vercel.app/api/scrape/status
```

**Deployment Architecture:**
```
Vercel Serverless Function
├── api/index.py (472 lines)
│   ├── FastAPI application
│   ├── get_scrape_response() helper
│   ├── 14 API endpoints
│   └── Imports main.py functions
└── main.py (Central Scraper Logic)
    ├── run_all_scrapers(return_json=True)
    ├── run_specific_scraper(site, return_json=True)
    ├── Shared with CLI usage
    └── Individual scrapers in scrapers/
```

**Deployment Benefits:**
- **Integrated Architecture**: CLI and API share the same scraping logic
- **Single Function**: All 14 endpoints served by one serverless function
- **Reduced Cold Starts**: Optimized single-file deployment
- **No Code Duplication**: main.py serves both CLI and API interfaces
- **Consistent Behavior**: Same scraping logic for local and production
- **Easy Maintenance**: Update scraping logic in main.py only
- **Python 3.9 Environment**: Configured in `vercel.json`
- **CORS Enabled**: All endpoints support cross-origin requests
- **Direct JSON Response**: No file storage for API endpoints

**Local vs Production:**
```bash
# Local Development (CLI - saves to files)
python main.py --site detik --format json
# Output: data/news_detik_20251218.json

# Production API (real-time JSON response)
curl https://your-app.vercel.app/api/scrape/detik
# Output: Direct JSON response (no files)

# Same underlying logic from main.py!
```

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
│   ├── tempo_scraper.py
│   └── kumparan_scraper.py
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
- `GET /api/scrape/all` - **Scrape all news sites**
- `GET /api/scrape/detik` - **Scrape Detik.com**
- `GET /api/scrape/kompas` - **Scrape Kompas.com**
- `GET /api/scrape/cnn` - **Scrape CNN Indonesia**
- `GET /api/scrape/antara` - **Scrape Antara News**
- `GET /api/scrape/tempo` - **Scrape Tempo**
- `GET /api/scrape/kumparan` - **Scrape Kumparan**
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
3. Add the scraper to `main.py` following the integrated pattern:
   - Implement a `scrape_<sitename>()` function in the scraper file
   - Add the scraper import to the `SCRAPERS` dictionary in `main.py`
   - Add the scraper to the available sites list in API documentation
4. Add the scraper endpoint to `api/index.py`:
   - Create a new endpoint using the `get_scrape_response()` helper
   - Follow the existing single-line pattern
5. Test thoroughly locally and on Vercel
6. Submit a pull request

**Example for Adding New Scraper:**

**Step 1: Add to main.py**
```python
# Add import at the top with other scrapers
from scrapers.newsite_scraper import scrape_newsite

# Add to SCRAPERS dictionary
SCRAPERS = {
    'kompas': scrape_kompas,
    'cnn': scrape_cnn,
    'antara': scrape_antara,
    'narasi': scrape_narasi,
    'tribun': scrape_tribun,
    'detik': scrape_detik,
    'newsite': scrape_newsite  # Add new scraper
}
```

**Step 2: Add endpoint to api/index.py**
```python
@app.get("/api/scrape/newsite")
async def scrape_newsite_endpoint():
    """Scrape NewSite and return JSON response using main.py logic"""
    return get_scrape_response(site_name='newsite')
```

**Step 3: Update API documentation**
- Add to sources list in `/api/sources` endpoint
- Add to documentation in `/api/scrape/status` endpoint

## Architecture Overview

### Integrated Flow Architecture

This project uses an **integrated flow architecture** where `main.py` serves as the central scraper logic for both CLI and API usage. This approach eliminates code duplication and provides consistent data structure across all interfaces.

**Flow Components:**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Usage     │    │   main.py        │    │   API Usage     │
│                 │    │ (Central Logic)  │    │                 │
│ python main.py  │◄──►│                  │◄──►│ /api/scrape/*   │
│ --site detik    │    │ - run_all_       │    │ endpoints       │
│ --format json   │    │   scrapers()     │    │                 │
│                 │    │ - run_specific_  │    │ JSON Response   │
│ Save to file    │    │   scraper()      │    │ (no file)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ File Storage    │    │   Individual     │    │ Direct JSON     │
│ (CSV/JSON/Excel)│    │   Scrapers       │    │ Response        │
│                 │    │   scrapers/      │    │                 │
│ data/ folder    │    │   directory      │    │ Real-time data  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

**Advantages of Integrated Architecture:**
- ✅ **Single Source of Truth**: All scraping logic centralized in `main.py`
- ✅ **No Code Duplication**: CLI and API share the same core functions
- ✅ **Consistent Data Structure**: Same response format across all interfaces
- ✅ **Easy Maintenance**: Update scraping logic in one place only
- ✅ **Backward Compatible**: CLI usage unchanged, API uses same logic
- ✅ **Direct JSON Response**: No file storage needed for API endpoints
- ✅ **Centralized Error Handling**: Comprehensive error management
- ✅ **Performance Tracking**: Site-specific execution metrics

**Main.py Architecture:**
```python
# main.py - Central scraper logic
├── Imports & Configuration
├── SCRAPERS Dictionary (6 news sites)
├── run_all_scrapers(return_json=False)
│   ├── CLI Mode: Save to file (default)
│   └── API Mode: Return JSON (return_json=True)
├── run_specific_scraper(site_name, return_json=False)
│   ├── CLI Mode: Save individual site to file
│   └── API Mode: Return individual site JSON
└── Helper Functions (logging, file operations, etc.)
```

**API Architecture (Single-File Design):**
```python
# api/index.py - 472 lines, 14 endpoints
├── Imports & FastAPI Setup
├── Data Models & CORS Configuration
├── Helper Function: get_scrape_response(site_name=None)
│   ├── Imports from main.py
│   ├── Handles both all-sites and individual scraping
│   ├── Returns JSONResponse with proper headers
│   └── Centralized error handling
├── Core API Endpoints (7 endpoints)
│   ├── GET / - Static data with filtering
│   ├── GET /api - Filtered articles
│   ├── GET /api/sources - Available sources
│   ├── GET /api/categories - Article categories
│   ├── GET /api/stats - Statistics
│   ├── GET /api/refresh - Refresh info
│   └── GET /health - Health check
└── Real-time Scraping Endpoints (7 endpoints)
    ├── GET /api/scrape/status - API documentation
    ├── GET /api/scrape/all - All sites via main.py
    ├── GET /api/scrape/detik - Detik.com via main.py
    ├── GET /api/scrape/kompas - Kompas.com via main.py
    ├── GET /api/scrape/cnn - CNN Indonesia via main.py
    ├── GET /api/scrape/antara - Antara News via main.py
    ├── GET /api/scrape/narasi - Narasi via main.py
    └── GET /api/scrape/tribun - Tribun News via main.py
```

**Request Flow:**
```
User Request → Vercel Router → api/index.py → get_scrape_response() → main.py → JSON Response
```

**Flow Examples:**

**API Request:**
```
GET /api/scrape/detik
└── api/index.py: scrape_detik_endpoint()
    └── get_scrape_response('detik')
        └── main.py: run_specific_scraper('detik', return_json=True)
            └── detik_scraper.py: scrape_detik()
                └── JSON Response (no file storage)
```

**CLI Request:**
```
python main.py --site detik --format json
└── main.py: run_specific_scraper('detik', return_json=False)
    └── detik_scraper.py: scrape_detik()
        └── Save to data/news_detik_YYYYMMDD.json
```

This integrated approach ensures that both CLI and API interfaces use the exact same scraping logic, making maintenance easier and ensuring consistency across all usage patterns.

### Integrated Flow Usage

**Dual Interface Design:**
The scraper supports both CLI and API interfaces with the same underlying logic:

#### CLI Interface (File Output)
```bash
# Traditional usage - saves to files
python main.py                           # All sites, default format
python main.py --site detik              # Individual site
python main.py --format csv              # CSV output
python main.py --format excel            # Excel output
python main.py --site kompas --format json  # Individual site + format
```

#### API Interface (Direct JSON Response)
```bash
# Real-time scraping - no files
curl https://your-app.vercel.app/api/scrape/all
curl https://your-app.vercel.app/api/scrape/detik
curl https://your-app.vercel.app/api/scrape/kompas
```

#### Programmatic Usage
```python
# Get JSON response directly (no files)
from main import run_all_scrapers, run_specific_scraper

# Scrape all sites
all_data = run_all_scrapers(return_json=True)
print(f"Total articles: {all_data['data']['metadata']['total_articles']}")

# Scrape individual site
detik_data = run_specific_scraper('detik', return_json=True)
articles = detik_data['data']['articles']
```

**Key Benefits of Integrated Design:**
- **Consistent Results**: Same data structure for CLI and API
- **No Duplication**: Single codebase for both interfaces
- **Flexible Output**: Files for batch processing, JSON for real-time
- **Easy Testing**: Test scraping logic independently
- **Unified Maintenance**: One place to update scraping logic

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