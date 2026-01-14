from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(Text)
    content = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    source_url = Column(String, unique=True, index=True)
    source_name = Column(String, index=True) # detik, kompas, etc.
    category = Column(String, index=True)
    region = Column(String, index=True, default="general") # mimika, timika, general
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
