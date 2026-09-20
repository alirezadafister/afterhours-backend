from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional

class EventResponse(BaseModel):
    id: UUID
    title: str
    venue: str
    event_date: date
    vibe: str
    description: Optional[str] = None
    created_at: datetime
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    venue: str
    event_date: date
    vibe: str
    description: Optional[str] = None
    image_url: Optional[str] = None

class EventUpdate(BaseModel):
    title: Optional[str] = None
    venue: Optional[str] = None
    event_date: Optional[date] = None
    vibe: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
