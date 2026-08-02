from uuid import UUID as PyUUID

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import DeliveryNotFoundError
from app.core.logging import get_logger
from app.models.delivery import Delivery, DeliveryStatus
from app.models.webhook_endpoint import WebhookEndpoint
from app.services.retries import calculate_next_retry, should_retry

logger = get_logger(__name__)


def create_deliveries(
    db: Session,
    event_id: PyUUID,
    endpoints: list[WebhookEndpoint],
) -> list[Delivery]:
    deliveries = []

    for endpoint in endpoints:
        delivery = Delivery(
            event_id=event_id,
            endpoint_id=endpoint.id,
        )
        deliveries.append(delivery)

    db.add_all(deliveries)

    logger.info(
        "Created %s deliveries for event %s",
        len(deliveries),
        event_id,
    )

    return deliveries


def get_deliveries(
    db: Session,
) -> list[Delivery]:
    return (
        db.query(Delivery)
        .order_by(Delivery.id.desc())
        .all()
    )


def get_delivery(
    db: Session,
    delivery_id: int,
) -> Delivery:
    delivery = (
        db.query(Delivery)
        .options(
            joinedload(Delivery.event),
            joinedload(Delivery.endpoint),
        )
        .filter(Delivery.id == delivery_id)
        .one_or_none()
    )

    if delivery is None:
        raise DeliveryNotFoundError(
            f"Delivery with id {delivery_id} not found"
        )

    return delivery


def mark_delivery_processing(
    delivery: Delivery,
) -> None:
    delivery.status = DeliveryStatus.PROCESSING
    delivery.next_retry_at = None

    logger.info(
        "Delivery %s marked as PROCESSING",
        delivery.id,
    )


def mark_delivery_success(
    delivery: Delivery,
) -> None:
    delivery.status = DeliveryStatus.SUCCESS
    delivery.next_retry_at = None

    logger.info(
        "Delivery %s marked as SUCCESS",
        delivery.id,
    )


def mark_delivery_failed(
    delivery: Delivery,
    last_error: str,
) -> None:
    delivery.status = DeliveryStatus.FAILED
    delivery.attempt_count += 1
    delivery.last_error = last_error

    logger.warning(
        "Delivery %s marked as FAILED (attempt %s): %s",
        delivery.id,
        delivery.attempt_count,
        last_error,
    )


def mark_delivery_dead_letter(
    delivery: Delivery,
) -> None:
    delivery.status = DeliveryStatus.DEAD_LETTER
    delivery.next_retry_at = None

    logger.error(
        "Delivery %s moved to DEAD_LETTER after %s attempts",
        delivery.id,
        delivery.attempt_count,
    )


def handle_delivery_failure(
    delivery: Delivery,
    last_error: str,
) -> None:
    mark_delivery_failed(
        delivery,
        last_error,
    )

    if should_retry(delivery):
        delivery.next_retry_at = calculate_next_retry(
            delivery.attempt_count,
        )

        logger.warning(
            "Retry #%s scheduled for delivery %s at %s",
            delivery.attempt_count + 1,
            delivery.id,
            delivery.next_retry_at.isoformat(),
        )

    else:
        mark_delivery_dead_letter(delivery)


def retry_delivery(
    delivery: Delivery,
) -> None:
    if delivery.status != DeliveryStatus.DEAD_LETTER:
        raise ValueError(
            "Only dead-letter deliveries can be manually retried."
        )

    logger.info(
        "Manual retry requested for delivery %s",
        delivery.id,
    )

    delivery.status = DeliveryStatus.PENDING
    delivery.next_retry_at = None