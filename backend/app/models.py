from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Anime(Base):
    __tablename__ = "animes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(Text, nullable=True)
    episodes = Column(Integer, nullable=True)
    status = Column(String(50), nullable=True)
    score = Column(Float, nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer)
    rank = Column(String(50))
    skins = Column(Text)
    price = Column(Float)
    description = Column(Text)
    contact_info = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    approved = Column(Boolean, default=False)
