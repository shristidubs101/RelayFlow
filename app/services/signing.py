import hashlib
import hmac
import json


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