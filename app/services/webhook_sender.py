from app.models.delivery import Delivery
from app.services.signing import generate_signature
import httpx


def send_webhook(
    delivery:Delivery,
)-> httpx.Response:
    
    signature = generate_signature(
        delivery.event.payload,
        delivery.endpoint.secret,
    )
    
    headers = {
        "X-RelayFlow-Signature": signature,
    }
    
    with httpx.Client(timeout=10.0) as client:
        response = client.post(
            delivery.endpoint.url,
            json = delivery.event.payload,
            headers = headers
        ) 
    
        return response