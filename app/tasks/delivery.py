from datetime import datetime, timezone

import httpx

from app.core.celery import celery_app
from app.db.session import SessionLocal
from app.services.deliveries import (
    get_delivery,
    handle_delivery_failure,
    mark_delivery_processing,
    mark_delivery_success,
)
from app.services.delivery_attempt import (
    create_delivery_attempt,
    mark_attempt_failed,
    mark_attempt_success,
)
from app.services.webhook_sender import send_webhook


@celery_app.task
def process_delivery(delivery_id: int):
    db = SessionLocal()

    try:
        delivery = get_delivery(db, delivery_id)
        mark_delivery_processing(delivery)

        # Create the attempt BEFORE making the HTTP call
        attempt = create_delivery_attempt(db, delivery)

        try:
            response = send_webhook(delivery)

            if response.is_success:
                mark_attempt_success(
                    attempt,
                    response.status_code,
                )
                mark_delivery_success(delivery)

            else:
                mark_attempt_failed(
                    attempt,
                    error=f"HTTP {response.status_code}",
                    status_code=response.status_code,
                )
                handle_delivery_failure(
                    delivery,
                    last_error=f"HTTP {response.status_code}",
                )

        except httpx.RequestError as e:
            # Network/timeout/SSL/DNS error — no response object exists
            mark_attempt_failed(
                attempt,
                error=str(e),
                status_code=None,
            )
            handle_delivery_failure(
                delivery,
                last_error=str(e),
            )

        db.commit()

        if delivery.next_retry_at is not None:
            print("NOW UTC:", datetime.now(timezone.utc))
            print("RETRY UTC:", delivery.next_retry_at)
            print(
                "SECONDS UNTIL RETRY:",
                (delivery.next_retry_at - datetime.now(timezone.utc)).total_seconds(),
            )

            process_delivery.apply_async(
                args=[delivery.id],
                eta=delivery.next_retry_at,
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()