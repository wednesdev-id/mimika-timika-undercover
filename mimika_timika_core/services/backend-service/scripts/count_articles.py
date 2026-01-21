import sys
import os
import logging

# Add parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models, database

def count_articles():
    db = database.SessionLocal()
    try:
        # Total
        total = db.query(models.Article).count()
        
        # Mimika (region='mimika' OR region='general' excluding 'timika')
        # Logic in main.py: 
        # mimika View = region IN ['mimika', 'general'] AND region != 'timika'
        # timika View = region IN ['timika', 'general'] AND region != 'mimika'
        
        # Actually storage is: 'mimika', 'timika', 'general'
        
        count_mimika_tagged = db.query(models.Article).filter(models.Article.region == 'mimika').count()
        count_timika_tagged = db.query(models.Article).filter(models.Article.region == 'timika').count()
        count_general = db.query(models.Article).filter(models.Article.region == 'general').count()
        
        print(f"--- DATABASE STATS ---")
        print(f"Total Articles: {total}")
        print(f"Tagged 'mimika': {count_mimika_tagged}")
        print(f"Tagged 'timika': {count_timika_tagged}")
        print(f"Tagged 'general': {count_general}")
        print(f"----------------------")
        print(f"Visible on Mimika Page ('mimika' + 'general'): {count_mimika_tagged + count_general}")
        print(f"Visible on Timika Page ('timika' + 'general'): {count_timika_tagged + count_general}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    count_articles()
