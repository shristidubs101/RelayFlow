from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db

from app.schemas.webhook_endpoint import (
    WebhookEndpointCreate,
    WebhookEndpointResponse,
    WebhookEndpointUpdate,
)

from app.services import webhook_endpoint


router = APIRouter()


@router.post(
    "/webhook-endpoints",
    response_model=WebhookEndpointResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_webhook_endpoint(
    endpoint: WebhookEndpointCreate,
    db: Session = Depends(get_db),
):
    return webhook_endpoint.create_webhook_endpoint(
        db=db,
        endpoint=endpoint,
    )


@router.get(
    "/webhook-endpoints",
    response_model=list[WebhookEndpointResponse],
)
def get_webhook_endpoints(
    db: Session = Depends(get_db),
):
    return webhook_endpoint.get_webhook_endpoints(
        db=db,
    )


@router.get(
    "/webhook-endpoints/{endpoint_id}",
    response_model=WebhookEndpointResponse,
)
def get_webhook_endpoint(
    endpoint_id: int,
    db: Session = Depends(get_db),
):
    return webhook_endpoint.get_webhook_endpoint(
        db=db,
        endpoint_id=endpoint_id,
    )


@router.patch(
    "/webhook-endpoints/{endpoint_id}",
    response_model=WebhookEndpointResponse,
)
def update_webhook_endpoint(
    endpoint_id: int,
    endpoint_update: WebhookEndpointUpdate,
    db: Session = Depends(get_db),
):
    return webhook_endpoint.update_webhook_endpoint(
        db=db,
        endpoint_id=endpoint_id,
        endpoint_update=endpoint_update,
    )


@router.delete(
    "/webhook-endpoints/{endpoint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_webhook_endpoint(
    endpoint_id: int,
    db: Session = Depends(get_db),
):
    webhook_endpoint.delete_webhook_endpoint(
        db=db,
        endpoint_id=endpoint_id,
    )
