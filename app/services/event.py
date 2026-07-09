from sqlalchemy.orm import Session

from app.models.event import Event
from app.schemas.events import EventCreate
from app.services.deliveries import create_deliveries
from app.services.webhook_endpoint import get_webhook_endpoints


def create_event(
    db: Session,
    event: EventCreate,
) -> Event:
    event_obj = Event(**event.model_dump())
    
    try:
        db.add(event_obj)
        db.flush()  # Flush to get the event ID before creating deliveries
        endpoints = get_webhook_endpoints(db)
        create_deliveries(db, event_obj.id, endpoints)
        db.commit()  # Commit the transaction to save the event and deliveries
        db.refresh(event_obj) 
        return event_obj
    
    except Exception:
        db.rollback()  # Rollback the transaction in case of an error
        raise