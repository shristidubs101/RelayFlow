from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DuplicateWebhookEndpointError
from app.models.webhook_endpoint import WebhookEndpoint
from app.schemas.webhook_endpoint import WebhookEndpointCreate

def create_webhook_endpoint(
    db: Session,
    endpoint: WebhookEndpointCreate,
) -> WebhookEndpoint:
    db_endpoint = WebhookEndpoint(**endpoint.model_dump(mode="json"))

    db.add(db_endpoint)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateWebhookEndpointError() from exc

    db.refresh(db_endpoint)
    return db_endpoint