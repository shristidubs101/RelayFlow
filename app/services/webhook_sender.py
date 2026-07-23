from app.models.delivery import Delivery
from app.services.signing import generate_signature
import httpx
import time


def send_webhook(
    delivery:Delivery,
)-> httpx.Response:
    timestamp = int(time.time())
    signature = generate_signature(
        delivery.event.payload,
        delivery.endpoint.secret,
        timestamp,
    )
    
    headers = {
        "X-RelayFlow-Timestamp": str(timestamp),
        "X-RelayFlow-Signature": signature,
    }
    
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            delivery.endpoint.url,
            json = delivery.event.payload,
            headers = headers
        ) 
    
        return response