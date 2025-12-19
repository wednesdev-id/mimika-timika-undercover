# Papua News - Project Documentation

## Overview

Papua News adalah sistem agregasi dan manajemen berita yang berfokus pada berita wilayah Papua/Mimika. Project ini terdiri dari tiga komponen utama yang bekerja sama untuk mengumpulkan, mengelola, dan menampilkan berita kepada publik.

## Arsitektur Project

### 🏗️ Komponen Utama

1. **mimika_scraping** - Python Backend (Scraping Engine)
   - FastAPI-based web scraping system
   - Mengumpulkan berita dari 6 sumber berita Indonesia utama
   - Pemrosesan data otomatis dan multiple format output

2. **mimika_dashboard** - React Admin Dashboard
   - Interface admin untuk verifikasi dan manajemen konten
   - Analytics dashboard dan publishing tools
   - Content management system

3. **mimika_landing_page** - React Public Website
   - Website publik untuk menampilkan berita
   - Search dan filtering functionality
   - Responsive design untuk mobile dan desktop

---

## 🚀 Fitur-Fitur Utama

### 1. News Scraping System (`mimika_scraping`)

#### 📰 Multi-Source Collection
- **6 Sumber Berita Utama**:
  - Detik.com
  - Kompas.com
  - CNN Indonesia
  - Antara News
  - Narasi
  - Tribun News

#### 🎯 Regional Focus
- **Target Keywords**: "mimika timika"
- **Geographic Filter**: Khusus berita wilayah Papua/Mimika
- **Content Relevance**: Otomatis filter berita relevan

#### 🔧 Data Processing
- **Deduplication**: Otomatis hapus berita duplikat
- **Data Cleaning**: Strukturasi dan pembersihan konten
- **Format Support**: JSON, CSV, dan Excel output
- **Validation**: Quality check dan data validation

#### ⏰ Automation Features
- **Scheduler**: Automated daily scraping
- **Logging System**: Comprehensive monitoring dan debugging
- **Error Handling**: Robust error recovery
- **Retry Logic**: Otomatis retry untuk failed requests

#### 🌐 API Endpoints
- **RESTful API**: FastAPI-based web interface
- **Data Retrieval**: JSON endpoints untuk frontend
- **Real-time Updates**: Live data fetching capability

### 2. Admin Dashboard (`mimika_dashboard`)

#### 📊 Dashboard Analytics
- **Main Overview**: Statistics dan insights
- **Data Visualization**: Charts dan graphs
- **Performance Metrics**: Scraping success rates
- **Content Analytics**: Article engagement tracking

#### 📝 Content Management
- **Scraped News Verification**:
  - Review interface untuk unverified content
  - Batch approval/rejection tools
  - Content editing dan modification

- **Verified News Management**:
  - Published content control
  - Scheduling system
  - Content categorization

#### 🔍 Search & Filter
- **Advanced Search**: Cari berita berdasarkan title, summary, category
- **Date Range Filter**: Filter berita berdasarkan tanggal
- **Category Filter**: Politik, Budaya, Sosial, Pendidikan, Lingkungan, Olahraga
- **Status Filter**: Verified/Unverified/Published

#### ⚙️ System Settings
- **Scraping Configuration**: Schedule dan source management
- **User Management**: Admin role dan permissions
- **Export Settings**: Output format preferences

### 3. Public Website (`mimika_landing_page`)

#### 🏠 User Interface
- **Hero Section**: "Portal Berita Timika & Mimika" branding
- **Modern Design**: Clean dan intuitive interface
- **Responsive Layout**: Mobile-first design approach
- **Dark/Light Mode**: Theme switching capability

#### 🔍 Search Functionality
- **Real-time Search**: Instant search results
- **Multi-field Search**: Title, summary, category search
- **Auto-complete**: Search suggestions
- **Search History**: Recent search tracking

#### 📂 Category System
- **6 Main Categories**:
  - Politik
  - Budaya
  - Sosial
  - Pendidikan
  - Lingkungan
  - Olahraga

#### 📰 News Display
- **Grid Layout**: Card-based article display
- **Article Cards**: Rich media preview
- **Load More**: Infinite scroll atau pagination
- **Popular News**: Trending articles sidebar

---

## 🛠️ Teknologi Stack

### Backend (`mimika_scraping`)
- **Python 3.7+**
- **FastAPI**: Web framework untuk API
- **Requests**: HTTP library untuk scraping
- **BeautifulSoup4**: HTML parsing
- **Python-dotenv**: Environment management
- **Pandas**: Data processing (optional)
- **Openpyxl**: Excel support (optional)
- **Schedule**: Task scheduling (optional)

### Frontend (`mimika_dashboard` & `mimika_landing_page`)
- **React 18.3.1** dengan TypeScript
- **Vite**: Build tool dan development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: Modern UI component library
- **React Router**: Client-side routing
- **React Query**: Data fetching dan caching
- **Radix UI**: Accessible component primitives

---

## 📁 Struktur File

```
Papua News/
├── mimika_scraping/              # Python backend
│   ├── scrapers/                # Individual site scrapers
│   │   ├── detik_scraper.py     # Detik.com scraper
│   │   ├── kompas_scraper.py    # Kompas.com scraper
│   │   ├── cnn_scraper.py       # CNN Indonesia scraper
│   │   ├── antara_scraper.py    # Antara News scraper
│   │   ├── narasi_scraper.py    # Narasi scraper
│   │   └── tribun_scraper.py    # Tribun News scraper
│   ├── utils/                   # Helper functions
│   │   ├── helpers.py           # Data processing utilities
│   │   └── scheduler.py         # Task scheduling
│   ├── api/                     # FastAPI web interface
│   │   └── index.py            # API endpoints
│   ├── data/                   # Output files directory
│   ├── logs/                   # Log files directory
│   ├── main.py                 # Main scraper orchestrator
│   └── requirements.txt        # Python dependencies
│
├── mimika_dashboard/            # React admin dashboard
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.tsx   # Main analytics dashboard
│   │   │   ├── ScrapedNews.tsx # Content verification interface
│   │   │   ├── VerifiedNews.tsx # Published content management
│   │   │   ├── Analytics.tsx   # Data visualization
│   │   │   └── Settings.tsx    # System configuration
│   │   ├── components/         # Reusable UI components
│   │   ├── components/ui/      # shadcn/ui components
│   │   └── App.tsx            # Main app component
│   ├── public/                 # Static assets
│   ├── package.json           # Node.js dependencies
│   └── vite.config.ts         # Vite configuration
│
└── mimika_landing_page/        # React public website
    ├── src/
    │   ├── pages/              # Main page components
    │   │   └── Index.tsx       # Landing page
    │   ├── components/         # Feature components
    │   │   ├── NewsCard.tsx    # Article display component
    │   │   ├── SearchBar.tsx   # Search functionality
    │   │   ├── CategoryFilter.tsx # Category filtering
    │   │   └── PopularNews.tsx # Trending articles sidebar
    │   ├── components/ui/      # shadcn/ui components
    │   └── data/               # News data storage
    ├── public/                 # Static assets
    ├── package.json           # Node.js dependencies
    └── vite.config.ts         # Vite configuration
```

---

## ⚙️ Konfigurasi & Setup

### Environment Variables

#### Backend (`.env`)
```env
# Output Configuration
OUTPUT_FORMAT=json
DATA_PATH=./data
LOG_PATH=./logs

# Scheduler Configuration
ENABLE_SCHEDULER=true
SCRAPE_INTERVAL=3600  # seconds

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

#### Frontend (`.env`)
```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000

# App Configuration
VITE_APP_NAME="Papua News"
VITE_APP_VERSION="1.0.0"
```

### Installation & Setup

#### Backend Setup
```bash
cd mimika_scraping
pip install -r requirements.txt
python main.py
```

#### Frontend Setup (Dashboard)
```bash
cd mimika_dashboard
npm install
npm run dev
```

#### Frontend Setup (Landing Page)
```bash
cd mimika_landing_page
npm install
npm run dev
```

---

## 🚀 Deployment Options

### Production Deployment

#### Backend Options
1. **Vercel** (Serverless) - Untuk demo/limited functionality
2. **Railway** (Recommended) - Full Python scraping functionality
3. **Render** - Alternative Python hosting
4. **PythonAnywhere** - Traditional Python hosting

#### Frontend Options
1. **Vercel** - Recommended untuk React apps
2. **Netlify** - Alternative static hosting
3. **AWS Amplify** - Full-stack deployment

#### Deployment Script Examples

##### Vercel Deployment
```bash
# Backend
vercel --prod

# Frontend Dashboard
cd mimika_dashboard
vercel --prod

# Frontend Landing
cd mimika_landing_page
vercel --prod
```

---

## 🔧 Maintenance & Monitoring

### Logging System
- **Access Logs**: API request tracking
- **Error Logs**: Scraping error monitoring
- **Performance Logs**: Response time tracking
- **Debug Logs**: Development troubleshooting

### Health Checks
- **API Status**: Endpoint availability monitoring
- **Scraper Health**: Source website accessibility
- **Data Quality**: Content validation checks
- **Performance Metrics**: System resource monitoring

### Backup & Recovery
- **Data Backup**: Automated database backups
- **Config Backup**: Configuration versioning
- **Recovery Procedures**: Disaster recovery plan
- **Redundancy**: Multi-region deployment options

---

## 📊 Performance & Analytics

### System Metrics
- **Scraping Success Rate**: % berhasil mengumpulkan berita
- **Data Freshness**: Frequency of content updates
- **API Response Time**: Backend performance metrics
- **User Engagement**: Website usage analytics

### Optimization Features
- **Caching**: React Query untuk data fetching
- **Lazy Loading**: Component-level code splitting
- **Image Optimization**: Compressed media delivery
- **CDN Integration**: Static asset distribution

---

## 🔒 Security Features

### Data Protection
- **Input Validation**: API request sanitization
- **Rate Limiting**: Abuse prevention
- **CORS Configuration**: Cross-origin security
- **Environment Variables**: Sensitive data protection

### Access Control
- **Admin Authentication**: Role-based access control
- **API Key Management**: Secure endpoint access
- **Session Management**: User session handling
- **Audit Logging**: Activity tracking

---

## 🚀 Future Enhancements

### Planned Features
1. **Mobile App**: React Native application
2. **Push Notifications**: Real-time news alerts
3. **AI Content Analysis**: Automatic content categorization
4. **Social Media Integration**: Content sharing capabilities
5. **Multi-language Support**: English & Indonesian options
6. **Advanced Analytics**: Google Analytics integration
7. **User Profiles**: Personalized news feeds
8. **Comment System**: User engagement features

### Scalability Improvements
1. **Database Integration**: PostgreSQL/MongoDB implementation
2. **Microservices Architecture**: Service separation
3. **Load Balancing**: Traffic distribution
4. **Container Deployment**: Docker/Kubernetes setup

---

## 📞 Support & Contact

### Documentation Resources
- **API Documentation**: OpenAPI/Swagger specification
- **Component Library**: Storybook documentation
- **Code Comments**: Inline code documentation
- **Wiki Pages**: Detailed feature guides

### Troubleshooting
- **Common Issues**: FAQ section
- **Error Codes**: Standardized error handling
- **Debug Mode**: Development troubleshooting tools
- **Support Channels**: Contact information for technical support

---

*Last Updated: November 2024*
*Version: 1.0.0*