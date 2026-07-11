from app.models.delivery import Delivery

import httpx


def send_webhook(
    delivery:Delivery,
)-> httpx.Response:
    with httpx.Client(timeout=10.0) as client:
        return client.post(
            delivery.endpoint.url,
            json=delivery.event.payload,
        )