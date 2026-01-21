import sys
import os
import logging

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models, database

def cleanup_junk_articles():
    db = database.SessionLocal()
    try:
        junk_keywords = [
            "tentang kami", "about us", "contact", "hubungi kami", "redaksi",
            "pedoman", "cyber media", "siber", "privacy", "kebijakan privasi",
            "disclaimer", "karir", "lowongan", "galeri foto", "video story",
            "term of use", "ketentuan", "indeks berita"
        ]
        
        print("Scanning for junk articles...")
        count = 0
        
        # Inefficient but safe: iterate and check (or use SQL LIKE)
        # Using SQL LIKE for major keywords to be faster
        for keyword in junk_keywords:
            # Check Title
            deleted = db.query(models.Article).filter(models.Article.title.ilike(f"%{keyword}%")).delete(synchronize_session=False)
            count += deleted
            # Check URL just in case
            deleted_url = db.query(models.Article).filter(models.Article.source_url.ilike(f"%{keyword}%")).delete(synchronize_session=False)
            count += deleted_url
            
        db.commit()
        print(f"Successfully deleted {count} junk articles/pages.")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_junk_articles()
