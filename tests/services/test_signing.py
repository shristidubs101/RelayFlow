import time

from app.services.signing import (
    generate_signature,
    verify_webhook,
)


def test_valid_webhook_signature():
    payload = {
        "user_id": 42,
        "plan": "Pro",
    }

    secret = "cheese"
    timestamp = int(time.time())

    signature = generate_signature(
        payload,
        secret,
        timestamp,
    )

    result = verify_webhook(
        payload,
        secret,
        timestamp,
        signature,
    )

    assert result is True

def test_tampered_payload_is_rejected():
    payload = {
        "user_id": 42,
        "plan": "Pro",
    }

    secret = "cheese"
    timestamp = int(time.time())

    signature = generate_signature(
        payload,
        secret,
        timestamp,
    )

    modified_payload = {
        "user_id": 42,
        "plan": "Enterprise",
    }

    result = verify_webhook(
        modified_payload,
        secret,
        timestamp,
        signature,
    )

    assert result is False

def test_wrong_secret_is_rejected():
    payload = {
        "user_id": 42,
        "plan": "Pro",
    }

    secret = "cheese"
    timestamp = int(time.time())

    signature = generate_signature(
        payload,
        secret,
        timestamp,
    )

    result = verify_webhook(
        payload,
        "wrong-secret",
        timestamp,
        signature,
    )

    assert result is False

def test_expired_timestamp_is_rejected():
    payload = {
        "user_id": 42,
        "plan": "Pro",
    }

    secret = "cheese"

    old_timestamp = int(time.time()) - 600

    signature = generate_signature(
        payload,
        secret,
        old_timestamp,
    )

    result = verify_webhook(
        payload,
        secret,
        old_timestamp,
        signature,
    )

    assert result is False

def test_changed_timestamp_is_rejected():
    payload = {
        "user_id": 42,
        "plan": "Pro",
    }

    secret = "cheese"
    timestamp = int(time.time())

    signature = generate_signature(
        payload,
        secret,
        timestamp,
    )

    result = verify_webhook(
        payload,
        secret,
        timestamp + 1,
        signature,
    )

    assert result is False