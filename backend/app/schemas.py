from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class AnimeBase(BaseModel):
    title: str
    description: Optional[str] = None
    episodes: Optional[int] = None
    status: Optional[str] = None
    score: Optional[float] = None
    image_url: Optional[str] = None

class AnimeCreate(AnimeBase):
    pass

class Anime(AnimeBase):
    id: int
    
    class Config:
        orm_mode = True

class AnimeList(BaseModel):
    animes: List[Anime]
