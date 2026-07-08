from app.models.webhook_endpoint import WebhookEndpoint
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID
from app.models.delivery import Delivery

def create_deliveries(
    db: Session,
    event_id: PyUUID,
    endpoints: list[WebhookEndpoint],
) -> list[Delivery]:
    deliveries = []
    for endpoint in endpoints:
        delivery = Delivery(
            event_id = event_id,
            endpoint_id = endpoint.id,
        )
        deliveries.append(delivery)
    db.add_all(deliveries)
    return deliveries