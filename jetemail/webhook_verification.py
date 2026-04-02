import hashlib
import hmac
import time


class WebhookSignatureVerificationFailed(Exception):
    """Raised when webhook signature verification fails."""

    pass


def verify_webhook(
    payload: bytes,
    signature: str,
    timestamp: str,
    secret: str,
    tolerance: int = 300,
) -> bool:
    """Verify a JetEmail webhook signature.

    This is a standalone utility that does not require a JetEmail client instance.
    It mirrors the verification logic from the Laravel SDK's VerifyWebhookSignature
    middleware.

    Args:
        payload: The raw request body bytes.
        signature: The value of the X-Webhook-Signature header.
        timestamp: The value of the X-Webhook-Timestamp header.
        secret: Your webhook signing secret.
        tolerance: Maximum age of the webhook in seconds (default: 300).

    Returns:
        True if the signature is valid.

    Raises:
        WebhookSignatureVerificationFailed: If the signature or timestamp is invalid.
    """
    # Check timestamp freshness
    try:
        ts = int(timestamp)
    except (ValueError, TypeError):
        raise WebhookSignatureVerificationFailed("Invalid timestamp.")

    if abs(time.time() - ts) > tolerance:
        raise WebhookSignatureVerificationFailed(
            "Webhook timestamp is outside the tolerance zone."
        )

    # Compute expected signature
    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison
    if not hmac.compare_digest(expected, signature):
        raise WebhookSignatureVerificationFailed("Invalid webhook signature.")

    return True
