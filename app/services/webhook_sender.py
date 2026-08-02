import time

import httpx

from app.core.logging import get_logger
from app.models.delivery import Delivery
from app.services.signing import generate_signature

logger = get_logger(__name__)


def send_webhook(
    delivery: Delivery,
) -> httpx.Response:
    timestamp = int(time.time())

    signature = generate_signature(
        delivery.event.payload,
        delivery.endpoint.secret,
        timestamp,
    )

    headers = {
        "X-RelayFlow-Timestamp": str(timestamp),
        "X-RelayFlow-Signature": signature,
        "X-RelayFlow-Event-ID": str(delivery.event.id),
    }

    logger.info(
        "Sending webhook for delivery %s to %s",
        delivery.id,
        delivery.endpoint.url,
    )

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                delivery.endpoint.url,
                json=delivery.event.payload,
                headers=headers,
            )

        logger.info(
            "Webhook for delivery %s returned HTTP %s",
            delivery.id,
            response.status_code,
        )

        return response

    except httpx.RequestError:
        logger.exception(
            "Network error while sending webhook for delivery %s",
            delivery.id,
        )
        raise