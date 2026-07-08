from pydantic.v1 import BaseModel, ConfigDict

from datetime import datetime
from typing import Any

from sqlalchemy import UUID

class EventCreate(BaseModel):
    event_type: str
    payload: dict[str, Any]
    
class EventResponse(BaseModel):
    id: UUID
    event_type: str
    payload: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)