from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.models.delivery_attempt import DeliveryAttempt, DeliveryAttemptStatus
from app.services.deliveries import get_delivery


def create_delivery_attempt(
    db: Session,
    delivery: Delivery,
) -> DeliveryAttempt:
    attempt = DeliveryAttempt(
        delivery_id=delivery.id,
        attempt_number=delivery.attempt_count + 1,
        status=DeliveryAttemptStatus.IN_PROGRESS,
    )

    db.add(attempt)
    db.flush()

    return attempt


def get_delivery_attempts(
    db: Session,
    delivery_id: int,
) -> list[DeliveryAttempt]:
    get_delivery(db, delivery_id)
    return (
        db.query(DeliveryAttempt)
        .filter(DeliveryAttempt.delivery_id == delivery_id)
        .order_by(DeliveryAttempt.attempt_number)
        .all()
    )


def mark_attempt_success(
    attempt: DeliveryAttempt,
    status_code: int,
) -> None:
    attempt.status = DeliveryAttemptStatus.SUCCESS
    attempt.status_code = status_code
    attempt.completed_at = datetime.now(timezone.utc)


def mark_attempt_failed(
    attempt: DeliveryAttempt,
    error: str,
    status_code: int | None = None,
) -> None:
    attempt.status = DeliveryAttemptStatus.FAILED
    attempt.status_code = status_code
    attempt.error = error
    attempt.completed_at = datetime.now(timezone.utc)
