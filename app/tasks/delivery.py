from datetime import datetime, timezone

import httpx

from app.core.celery import celery_app
from app.core.logging import get_logger
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

logger = get_logger(__name__)


@celery_app.task
def process_delivery(delivery_id: int):
    db = SessionLocal()

    try:
        logger.info(
            "Processing delivery %s",
            delivery_id,
        )

        delivery = get_delivery(db, delivery_id)

        mark_delivery_processing(delivery)

        logger.info(
            "Delivery %s marked as PROCESSING",
            delivery.id,
        )

        attempt = create_delivery_attempt(db, delivery)

        logger.info(
            "Created attempt #%s for delivery %s",
            attempt.attempt_number,
            delivery.id,
        )

        try:
            logger.info(
                "Sending webhook for delivery %s to %s",
                delivery.id,
                delivery.endpoint.url,
            )

            response = send_webhook(delivery)

            logger.info(
                "Received HTTP %s for delivery %s",
                response.status_code,
                delivery.id,
            )

            if response.is_success:
                mark_attempt_success(
                    attempt,
                    response.status_code,
                )

                mark_delivery_success(delivery)

                logger.info(
                    "Delivery %s completed successfully",
                    delivery.id,
                )

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

                logger.warning(
                    "Delivery %s failed with HTTP %s",
                    delivery.id,
                    response.status_code,
                )

        except httpx.RequestError as e:
            mark_attempt_failed(
                attempt,
                error=str(e),
                status_code=None,
            )

            handle_delivery_failure(
                delivery,
                last_error=str(e),
            )

            logger.error(
                "Network error while sending delivery %s: %s",
                delivery.id,
                str(e),
            )

        db.commit()

        logger.info(
            "Delivery %s committed to database",
            delivery.id,
        )

        if delivery.next_retry_at is not None:
            logger.warning(
                "Scheduling retry #%s for delivery %s at %s",
                delivery.attempt_count + 1,
                delivery.id,
                delivery.next_retry_at.isoformat(),
            )

            process_delivery.apply_async(
                args=[delivery.id],
                eta=delivery.next_retry_at,
            )

    except Exception:
        db.rollback()

        logger.exception(
            "Unexpected error while processing delivery %s",
            delivery_id,
        )

        raise

    finally:
        db.close()

        logger.debug(
            "Database session closed for delivery %s",
            delivery_id,
        )