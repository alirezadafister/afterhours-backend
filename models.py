
from sqlalchemy import Column, Text, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(Text, nullable=False)
    venue = Column(Text, nullable=False)
    event_date = Column(Date, nullable=False)
    vibe = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    image_url = Column(Text, nullable=True)
