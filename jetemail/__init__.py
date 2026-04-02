from .version import __version__
from ._client import JetEmail
from ._types import Attachment, SendEmailOptions
from .exceptions import JetEmailError, ApiKeyIsMissing
from .webhook_verification import verify_webhook, WebhookSignatureVerificationFailed

__all__ = [
    "__version__",
    "JetEmail",
    "Attachment",
    "SendEmailOptions",
    "JetEmailError",
    "ApiKeyIsMissing",
    "verify_webhook",
    "WebhookSignatureVerificationFailed",
]
