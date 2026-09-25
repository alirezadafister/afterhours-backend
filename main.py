from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Event
from schemas import EventResponse, EventCreate, EventUpdate
from supabase_client import supabase
from typing import List
from uuid import UUID, uuid4
from datetime import datetime, timezone
import time

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://after-hour-wine.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/events", response_model=List[EventResponse])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).all()

@app.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: UUID, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    new_event = Event(
        id=uuid4(),
        title=event.title,
        venue=event.venue,
        event_date=event.event_date,
        vibe=event.vibe,
        description=event.description,
        image_url=event.image_url,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@app.put("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: UUID, event: EventUpdate, db: Session = Depends(get_db)):
    existing_event = db.query(Event).filter(Event.id == event_id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    update_data = event.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_event, key, value)

    db.commit()
    db.refresh(existing_event)
    return existing_event

@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: UUID, db: Session = Depends(get_db)):
    existing_event = db.query(Event).filter(Event.id == event_id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(existing_event)
    db.commit()
    return None

@app.post("/upload-image")
def upload_image(file: UploadFile = File(...)):
    file_bytes = file.file.read()
    file_name = f"{int(time.time())}-{file.filename}"

    supabase.storage.from_("event-images").upload(
        file_name, file_bytes, {"content-type": file.content_type} # type: ignore
    )

    public_url = supabase.storage.from_("event-images").get_public_url(file_name)
    return {"image_url": public_url}
