from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import DuplicateWebhookEndpointError, WebhookEndpointNotFoundError
from app.models.webhook_endpoint import WebhookEndpoint
from app.schemas.webhook_endpoint import WebhookEndpointCreate, WebhookEndpointUpdate

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



def get_webhook_endpoints(
    db:Session
) ->list[WebhookEndpoint]:
    endpoints =( db.query(WebhookEndpoint).
                filter(WebhookEndpoint.is_active.is_(True)).
                order_by(WebhookEndpoint.id.asc())
                .all()
            )
    return endpoints



def get_webhook_endpoint(
    db: Session,
    endpoint_id: int,
) -> WebhookEndpoint:
    endpoint = db.get(WebhookEndpoint, endpoint_id)

    if endpoint is None or not endpoint.is_active:
        raise WebhookEndpointNotFoundError()

    return endpoint



def update_webhook_endpoint(
    db : Session,
    endpoint_id: int,
    endpoint_update: WebhookEndpointUpdate,
    ) -> WebhookEndpoint:
    endpoint = get_webhook_endpoint(db, endpoint_id)
    
    update_data = endpoint_update.model_dump(exclude_unset=True, mode="json")
    
    for key, value in update_data.items():
        setattr(endpoint, key, value)
        
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateWebhookEndpointError() from exc
    
    db.refresh(endpoint)
    return endpoint



def delete_webhook_endpoint(
    db : Session, 
    endpoint_id: int
) -> None:
    endpoint = get_webhook_endpoint(db, endpoint_id)
    endpoint.is_active = False
    db.commit()