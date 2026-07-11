from app.models.webhook_endpoint import WebhookEndpoint
from sqlalchemy.orm import Session, joinedload
from uuid import UUID as PyUUID
from app.models.delivery import Delivery, DeliveryStatus

from app.core.exceptions import DeliveryNotFoundError

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

def get_delivery(
    db: Session,
    delivery_id: int,
) -> Delivery:
    delivery = db.query(Delivery).options(
        joinedload(Delivery.event),
        joinedload(Delivery.endpoint)
    ).filter(Delivery.id == delivery_id).one_or_none()
    
    if delivery is None:
        raise DeliveryNotFoundError(f"Delivery with id {delivery_id} not found")
    
    return delivery

def mark_delivery_processing(
    delivery: Delivery,
) -> None:
    delivery.status = DeliveryStatus.PROCESSING
    
def mark_delivery_success(
    delivery: Delivery,
) -> None:
    delivery.status = DeliveryStatus.SUCCESS