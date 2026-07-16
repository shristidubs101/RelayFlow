from datetime import datetime, timedelta, timezone
from app.models.delivery import Delivery

BASE_RETRY_DELAY = 30      # seconds
MAX_RETRY_DELAY = 240      # seconds
MAX_ATTEMPTS = 5

def calculate_next_retry(
    attempt_count: int
) -> datetime:    
    delay = min(
        BASE_RETRY_DELAY * (2 ** (attempt_count-1)),
        MAX_RETRY_DELAY,
    )
    
    return datetime.now(timezone.utc) + timedelta(seconds=delay)


def should_retry(
    delivery: Delivery,
) -> bool:
    attempt_count = delivery.attempt_count
    return delivery.attempt_count < MAX_ATTEMPTS