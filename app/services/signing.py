import json, time, hmac, hashlib


def generate_signature(
    payload: dict,
    secret: str,
    timestamp: int,
) -> str:
    payload_json = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
    )

    signed_payload = f"{timestamp}.{payload_json}"

    signature = hmac.new(
        secret.encode("utf-8"),
        signed_payload.encode("utf-8"),
        hashlib.sha256,
    )

    return signature.hexdigest()

def verify_signature(
    payload: dict,
    secret: str,
    timestamp: int,
    received_signature: str,
) -> bool:
    expected_signature = generate_signature(
        payload,
        secret,
        timestamp,
    )
    
    return hmac.compare_digest(
        expected_signature,
        received_signature,
    )
    
def is_timestamp_valid(
    timestamp: int,
    tolerance: int = 300,
) -> bool:
    current_time = int(time.time())

    return abs(current_time - timestamp) <= tolerance

def verify_webhook(
    payload: dict,
    secret: str,
    timestamp: int,
    received_signature: str,
) -> bool:
    if not is_timestamp_valid(timestamp):
        return False

    return verify_signature(
        payload,
        secret,
        timestamp,
        received_signature,
        )