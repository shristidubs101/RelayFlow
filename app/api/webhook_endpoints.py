from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.exceptions import DuplicateWebhookEndpointError
from app.schemas.webhook_endpoint import (
    WebhookEndpointCreate,
    WebhookEndpointResponse,
)
from app.services import webhook_endpoint

router = APIRouter()


@router.post(
    "/webhook-endpoints",
    response_model=WebhookEndpointResponse,
    status_code=201,
)
def create_webhook_endpoint(
    endpoint: WebhookEndpointCreate,
    db: Session = Depends(get_db),
):
    try:
        return webhook_endpoint.create_webhook_endpoint(
            db=db,
            endpoint=endpoint,
        )
    except DuplicateWebhookEndpointError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )