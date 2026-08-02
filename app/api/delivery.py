from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.delivery import (
    DeliveryAttemptResponse,
    DeliveryDetailResponse,
    DeliveryResponse,
)
from app.services import deliveries, delivery_attempt
from app.tasks.delivery import process_delivery

router = APIRouter()


@router.get(
    "/deliveries",
    response_model=list[DeliveryResponse],
)
def get_deliveries(
    db: Session = Depends(get_db),
):
    return deliveries.get_deliveries(
        db=db,
    )


@router.get(
    "/deliveries/{delivery_id}",
    response_model=DeliveryDetailResponse,
)
def get_delivery(
    delivery_id: int,
    db: Session = Depends(get_db),
):
    return deliveries.get_delivery(
        db=db,
        delivery_id=delivery_id,
    )


@router.get(
    "/deliveries/{delivery_id}/attempts",
    response_model=list[DeliveryAttemptResponse],
)
def get_delivery_attempts(
    delivery_id: int,
    db: Session = Depends(get_db),
):
    return delivery_attempt.get_delivery_attempts(
        db=db,
        delivery_id=delivery_id,
    )


@router.post(
    "/deliveries/{delivery_id}/retry",
    response_model=DeliveryResponse,
)
def retry_delivery_endpoint(
    delivery_id: int,
    db: Session = Depends(get_db),
):
    delivery = deliveries.get_delivery(
        db=db,
        delivery_id=delivery_id,
    )

    deliveries.retry_delivery(
        delivery=delivery,
    )

    db.commit()

    process_delivery.delay(delivery.id)

    db.refresh(delivery)

    return delivery