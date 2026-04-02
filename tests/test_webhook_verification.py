import hashlib
import hmac as hmac_mod
import time

import pytest

from jetemail.webhook_verification import (
    verify_webhook,
    WebhookSignatureVerificationFailed,
)


def _sign(payload: bytes, secret: str, timestamp: int) -> str:
    """Helper to produce a valid signature."""
    return "sha256=" + hmac_mod.new(
        secret.encode("utf-8"), payload, hashlib.sha256
    ).hexdigest()


class TestWebhookVerification:
    def test_valid_signature(self):
        secret = "whsec_test123"
        payload = b'{"type":"outbound.delivered","data":{}}'
        ts = str(int(time.time()))
        sig = _sign(payload, secret, int(ts))

        assert verify_webhook(payload, sig, ts, secret) is True

    def test_invalid_signature(self):
        secret = "whsec_test123"
        payload = b'{"type":"outbound.delivered","data":{}}'
        ts = str(int(time.time()))

        with pytest.raises(WebhookSignatureVerificationFailed, match="Invalid webhook signature"):
            verify_webhook(payload, "sha256=bad", ts, secret)

    def test_expired_timestamp(self):
        secret = "whsec_test123"
        payload = b'{"type":"outbound.delivered","data":{}}'
        old_ts = str(int(time.time()) - 600)
        sig = _sign(payload, secret, int(old_ts))

        with pytest.raises(WebhookSignatureVerificationFailed, match="tolerance"):
            verify_webhook(payload, sig, old_ts, secret)

    def test_invalid_timestamp(self):
        secret = "whsec_test123"
        payload = b'{"type":"outbound.delivered","data":{}}'

        with pytest.raises(WebhookSignatureVerificationFailed, match="Invalid timestamp"):
            verify_webhook(payload, "sha256=abc", "not-a-number", secret)

    def test_custom_tolerance(self):
        secret = "whsec_test123"
        payload = b'{"type":"outbound.delivered","data":{}}'
        ts = str(int(time.time()) - 400)
        sig = _sign(payload, secret, int(ts))

        # Should fail with default tolerance (300s)
        with pytest.raises(WebhookSignatureVerificationFailed):
            verify_webhook(payload, sig, ts, secret, tolerance=300)

        # Should pass with larger tolerance
        assert verify_webhook(payload, sig, ts, secret, tolerance=500) is True


class TestAttachment:
    def test_from_content_string(self):
        from jetemail import Attachment

        att = Attachment.from_content("hello world", "test.txt")
        assert att.filename == "test.txt"
        assert att.data  # base64 encoded

    def test_from_content_bytes(self):
        from jetemail import Attachment

        att = Attachment.from_content(b"hello world", "test.txt")
        assert att.filename == "test.txt"

    def test_from_path(self, tmp_path):
        from jetemail import Attachment

        f = tmp_path / "sample.txt"
        f.write_text("sample content")

        att = Attachment.from_path(str(f))
        assert att.filename == "sample.txt"
        assert att.data

    def test_from_path_custom_name(self, tmp_path):
        from jetemail import Attachment

        f = tmp_path / "sample.txt"
        f.write_text("sample content")

        att = Attachment.from_path(str(f), filename="custom.txt")
        assert att.filename == "custom.txt"

    def test_to_dict(self):
        from jetemail import Attachment

        att = Attachment(filename="test.txt", data="YWJj")
        assert att.to_dict() == {"filename": "test.txt", "data": "YWJj"}


class TestClientInit:
    def test_missing_api_key_raises(self):
        from jetemail import JetEmail, ApiKeyIsMissing

        with pytest.raises(ApiKeyIsMissing):
            JetEmail(api_key="")

    def test_client_creates_resources(self):
        from jetemail import JetEmail
        from jetemail.emails import Emails
        from jetemail.batch import Batch

        client = JetEmail(api_key="test_key_123")
        assert isinstance(client.emails, Emails)
        assert isinstance(client.batch, Batch)
