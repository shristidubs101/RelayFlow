from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from app.db.session import get_db
from app.schemas.events import EventCreate, EventResponse

from app.services import event


router = APIRouter()

@router.post(
    "/event",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_: EventCreate,
    db: Session = Depends(get_db),
)-> EventResponse:
    return event.create_event(
        db=db,
        event=event_,
    )

@router.get(
    "/events",
    response_model=list[EventResponse],
)
def get_events(
    db: Session = Depends(get_db),
):
    return event.get_events(
        db=db,
    )