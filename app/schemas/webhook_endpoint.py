from datetime import datetime
from pydantic import BaseModel, HttpUrl, ConfigDict


class WebhookEndpointCreate(BaseModel):
    url: HttpUrl
    secret: str


class WebhookEndpointResponse(BaseModel):
    id: int
    url: HttpUrl
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)