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

- **Multiple Output Formats**:
  - JSON (default) - structured format with metadata
  - CSV - for spreadsheet analysis
  - Excel - for data analysis in Excel

- **Web Interface**: Beautiful, responsive web viewer with:
  - 🔍 Search functionality
  - 📂 Category filtering
  - 📡 Source filtering
  - 📊 Statistics dashboard
  - 📱 Mobile-responsive design

- **Advanced Features**:
  - ✅ Modular architecture - each site has its own scraper
  - ✅ Automatic duplicate removal based on URLs
  - ✅ Built-in scheduler for automated daily scraping
  - ✅ Comprehensive logging system
  - ✅ CLI interface for flexible usage
  - ✅ Random delays to respect server rate limits
  - ✅ Error handling and recovery

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

### 1. Run Scraping

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

### 2. Start Web Viewer

**Start the web interface:**
```bash
python web_viewer.py
```

Then open your browser and go to: `http://localhost:5000`

### 3. Environment Variables (Optional)

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
Papua News/
├── main.py              # Main scraper script
├── web_viewer.py        # Flask web application
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── data/               # Output files (CSV, JSON, Excel)
├── logs/               # Log files
├── templates/          # HTML templates for web viewer
│   └── index.html
├── scrapers/           # Individual news site scrapers
│   ├── detik_scraper.py
│   ├── kompas_scraper.py
│   ├── cnn_scraper.py
│   ├── antara_scraper.py
│   ├── narasi_scraper.py
│   └── tribun_scraper.py
└── utils/              # Helper functions
    ├── helpers.py      # Data processing utilities
    └── scheduler.py    # Task scheduling
```

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

## Contributing

1. Fork the repository
2. Create a new scraper in the `scrapers/` directory
3. Follow the existing pattern: implement a `scrape_<sitename>()` function
4. Add the scraper to `main.py`
5. Test thoroughly
6. Submit a pull request

## Best Practices

- ⚠️ Respect website robots.txt files
- ⚠️ Use appropriate delays between requests
- ⚠️ Don't overload servers
- ⚠️ Consider fair use policies
- ⚠️ Monitor logs regularly

## Troubleshooting

### Common Issues

1. **No articles scraped**: Check if website structure has changed
2. **Connection timeouts**: Increase timeout values or check internet connection
3. **Rate limiting**: Increase delay values between requests
4. **Missing dependencies**: Run `pip install -r requirements.txt`

### Debug Mode

Enable debug logging by modifying `utils/helpers.py`:
```python
logging.basicConfig(level=logging.DEBUG)
```

## License

This project is for educational and research purposes. Users are responsible for complying with the terms of service of the target websites.

## Disclaimer

This tool should be used responsibly and in accordance with the terms of service of the target websites. The authors are not responsible for any misuse of this software.