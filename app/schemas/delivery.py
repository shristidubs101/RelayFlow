from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.delivery import DeliveryStatus
from app.models.delivery_attempt import DeliveryAttemptStatus
from app.schemas.events import EventResponse
from app.schemas.webhook_endpoint import WebhookEndpointResponse


class DeliveryResponse(BaseModel):
    id: int
    event_id: UUID
    endpoint_id: int

    status: DeliveryStatus
    attempt_count: int

    last_error: str | None
    next_retry_at: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class DeliveryDetailResponse(BaseModel):
    id: int

    event_id: UUID
    endpoint_id: int

    status: DeliveryStatus
    attempt_count: int
    last_error: str | None
    next_retry_at: datetime | None

    created_at: datetime
    updated_at: datetime

    event: EventResponse
    endpoint: WebhookEndpointResponse

    model_config = ConfigDict(from_attributes=True)


class DeliveryAttemptResponse(BaseModel):
    id: int
    delivery_id: int
    attempt_number: int

    status: DeliveryAttemptStatus
    status_code: int | None
    error: str | None

    started_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
