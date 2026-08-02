from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    DuplicateWebhookEndpointError,
    WebhookEndpointNotFoundError,
)
from app.core.logging import get_logger
from app.models.webhook_endpoint import WebhookEndpoint
from app.schemas.webhook_endpoint import (
    WebhookEndpointCreate,
    WebhookEndpointUpdate,
)

logger = get_logger(__name__)


def create_webhook_endpoint(
    db: Session,
    endpoint: WebhookEndpointCreate,
) -> WebhookEndpoint:

    db_endpoint = WebhookEndpoint(
        **endpoint.model_dump(mode="json")
    )

    db.add(db_endpoint)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        logger.warning(
            "Attempted to create duplicate webhook endpoint: %s",
            endpoint.url,
        )
        raise DuplicateWebhookEndpointError() from exc

    db.refresh(db_endpoint)

    logger.info(
        "Webhook endpoint %s created (id=%s)",
        db_endpoint.url,
        db_endpoint.id,
    )

    return db_endpoint


def get_webhook_endpoints(
    db: Session,
) -> list[WebhookEndpoint]:

    return (
        db.query(WebhookEndpoint)
        .filter(
            WebhookEndpoint.is_active.is_(True)
        )
        .order_by(
            WebhookEndpoint.id.asc()
        )
        .all()
    )


def get_webhook_endpoint(
    db: Session,
    endpoint_id: int,
) -> WebhookEndpoint:

    endpoint = db.get(
        WebhookEndpoint,
        endpoint_id,
    )

    if endpoint is None or not endpoint.is_active:
        raise WebhookEndpointNotFoundError()

    return endpoint


def update_webhook_endpoint(
    db: Session,
    endpoint_id: int,
    endpoint_update: WebhookEndpointUpdate,
) -> WebhookEndpoint:

    endpoint = get_webhook_endpoint(
        db,
        endpoint_id,
    )

    update_data = endpoint_update.model_dump(
        exclude_unset=True,
        mode="json",
    )

    for key, value in update_data.items():
        setattr(endpoint, key, value)

    try:
        db.commit()

    except IntegrityError as exc:
        db.rollback()
        logger.warning(
            "Attempted to update webhook endpoint %s with duplicate URL",
            endpoint_id,
        )
        raise DuplicateWebhookEndpointError() from exc

    db.refresh(endpoint)

    logger.info(
        "Webhook endpoint %s updated",
        endpoint.id,
    )

    return endpoint


def delete_webhook_endpoint(
    db: Session,
    endpoint_id: int,
) -> None:

    endpoint = get_webhook_endpoint(
        db,
        endpoint_id,
    )

    endpoint.is_active = False

    db.commit()

    logger.info(
        "Webhook endpoint %s deactivated",
        endpoint.id,
    )