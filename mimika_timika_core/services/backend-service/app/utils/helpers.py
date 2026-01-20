"""
Helper functions for news scraping - Optimized for JSON-only responses
"""

import re
import logging
import json
from datetime import datetime
from typing import List, Dict, Any
import os

def setup_logging():
    """Setup logging configuration"""
    handlers = [logging.StreamHandler()]
    
    # Try to add file handler, but don't fail if filesystem is read-only (e.g., Vercel)
    try:
        os.makedirs('logs', exist_ok=True)
        handlers.append(logging.FileHandler('logs/scrape_log.txt'))
    except (OSError, PermissionError):
        # Serverless environments like Vercel have read-only filesystems
        # Just use console logging
        pass
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    return logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters"""
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    return text

def extract_date(date_text: str) -> datetime:
    """Extract and standardize date from text"""
    if not date_text:
        return datetime.now()

    # Common Indonesian date formats
    date_patterns = [
        r'(\d{1,2})/(\d{1,2})/(\d{4})',  # DD/MM/YYYY
        r'(\d{1,2})-(\d{1,2})-(\d{4})',  # DD-MM-YYYY
        r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
    ]

    for pattern in date_patterns:
        match = re.search(pattern, date_text)
        if match:
            try:
                if pattern == date_patterns[0] or pattern == date_patterns[1]:
                    day, month, year = map(int, match.groups())
                else:
                    year, month, day = map(int, match.groups())
                return datetime(year, month, day)
            except ValueError:
                continue

    return datetime.now()

def remove_duplicates(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate articles based on URL"""
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    return unique_articles

def log_site_status(site_name: str, status: str, error_msg: str = None):
    """Log scraping status for each site"""
    if status == "OK":
        logging.info(f"[{site_name}] Scraping completed successfully")
    else:
        logging.error(f"[{site_name}] Scraping failed: {error_msg}")

def validate_article(article: Dict[str, Any]) -> bool:
    """Validate if article has required fields"""
    required_fields = ['title', 'url']

    for field in required_fields:
        if not article.get(field):
            return False

    return True

    return True

def normalize_category(category: str, title: str = "", url: str = "") -> str:
    """
    Standardize category names.
    If 'category' is generic (e.g. 'news'), tries to deduce from 'title' or 'url'.
    """
    # 1. Prepare classification text (Category + Title + URL) to search keywords in
    # specific_category takes precedence if it's not generic
    cat_lower = category.lower().strip() if category else ""
    
    # List of generic categories that don't mean much
    generics = ["news", "berita", "artikel", "index", "search", "", "nasional", "umum"]
    
    classification_text = cat_lower
    if cat_lower in generics:
        # If category is generic, rely heavily on title and url
        classification_text = f"{cat_lower} {title.lower()} {url.lower()}"
    else:
        # If category is specific, we still check title/url for 'Regional' context
        classification_text = f"{cat_lower} {title.lower()} {url.lower()}"

    # 2. Priority: Regional (Mimika/Timika)
    if any(x in classification_text for x in ["mimika", "timika", "papua", "jayapura", "regional", "daerah"]):
        return "Regional"

    # 3. Category Mappings
    mappings = {
        "Hukum & Kriminal": ["hukum", "kriminal", "polisi", "pengadilan", "kehakiman", "pidana", "perdata", "tewas", "dibunuh", "pembunuhan", "narkoba", "korupsi", "kpk", "polres", "polda"],
        "Pemerintahan": ["pemerintah", "politik", "dprd", "bupati", "pemda", "birokrasi", "kebijakan", "jokowi", "menteri", "partai", "pilkada", "pemilu"],
        "Ekonomi": ["ekonomi", "bisnis", "keuangan", "finansial", "pasar", "saham", "properti", "industri", "dagang", "umkm", "investasi", "modal", "harga"],
        "Olahraga": ["olahraga", "bola", "sport", "sepakbola", "badminton", "atlet", "pssi", "liga", "pertandingan"],
        "Pendidikan": ["pendidikan", "sekolah", "kampus", "kuliah", "edukasi", "guru", "siswa", "mahasiswa", "beasiswa", "pelajar"],
        "Kesehatan": ["kesehatan", "medis", "dokter", "rumah sakit", "rsud", "penyakit", "obat", "stunting", "vaksin", "puskesmas"],
        "Sosial & Budaya": ["sosial", "budaya", "seni", "hiburan", "lifestyle", "gaya hidup", "travel", "wisata", "seleb", "artis", "adat", "warga"],
        "Teknologi": ["teknologi", "tekno", "sains", "gadget", "internet", "digital", "aplikasi", "sistem", "cyber"],
        "Lingkungan": ["lingkungan", "alam", "forestri", "hutan", "cuaca", "bencana", "banjir", "gempa", "sampah", "konservasi"],
        "Otomotif": ["otomotif", "motor", "mobil", "kendaraan"],
        "Opini": ["opini", "tajuk", "kolom", "surat pembaca", "editorial"]
    }
    
    for standard, keywords in mappings.items():
        for keyword in keywords:
            # Check with word boundary logic simply by ensuring it's in the text
            if keyword in classification_text:
                return standard
                
    # 4. Fallback
    # If the original category was not generic and didn't match anything, keep it (capitalized)
    if cat_lower and cat_lower not in generics and len(cat_lower) < 20:
        return category.title()
        
    return "Nasional"

def validate_source(url: str) -> bool:
    """Validate if the source URL is acceptable"""
    if not url or not url.startswith('http'):
        return False
    
    # Block list (optional, e.g. known bad subdomains or aggregators)
    blocked_terms = ['doubleclick', 'googleadservices', 'iklan', 'ads']
    for term in blocked_terms:
        if term in url.lower():
            return False
            
    return True