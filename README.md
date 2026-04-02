# JetEmail Python SDK

The official Python SDK for [JetEmail](https://jetemail.com) transactional email.

## Installation

```bash
pip install jetemail
```

## Quick Start

```python
from jetemail import JetEmail, SendEmailOptions

client = JetEmail(api_key="your_api_key")

result = client.emails.send(
    SendEmailOptions(
        from_="you@yourdomain.com",
        to="recipient@example.com",
        subject="Hello from JetEmail",
        html="<p>Welcome!</p>",
    )
)

print(result["id"])
```

## Send an Email

```python
from jetemail import JetEmail, SendEmailOptions, Attachment

client = JetEmail(api_key="your_api_key")

client.emails.send(
    SendEmailOptions(
        from_="You <you@yourdomain.com>",
        to=["alice@example.com", "bob@example.com"],
        subject="Monthly Report",
        html="<h1>Report</h1><p>See attached.</p>",
        text="Report - see attached.",
        cc="manager@example.com",
        bcc="archive@example.com",
        reply_to="support@yourdomain.com",
        headers={"X-Entity-Ref-ID": "report-2025-01"},
        attachments=[
            Attachment.from_path("/path/to/report.pdf"),
            Attachment.from_content("raw,csv,data", "data.csv"),
        ],
    )
)
```

## Send Batch Emails

Send up to 100 emails in a single API call:

```python
from jetemail import JetEmail, SendEmailOptions

client = JetEmail(api_key="your_api_key")

emails = [
    SendEmailOptions(
        from_="you@yourdomain.com",
        to=recipient,
        subject="Hello!",
        html=f"<p>Hi {name}!</p>",
    )
    for name, recipient in [("Alice", "alice@example.com"), ("Bob", "bob@example.com")]
]

result = client.batch.send(emails)
print(result["summary"])
```

## Webhook Verification

Verify incoming webhook signatures without a client instance:

```python
from jetemail import verify_webhook
from jetemail.webhook_verification import WebhookSignatureVerificationFailed

try:
    verify_webhook(
        payload=request.body,             # raw bytes
        signature=request.headers["X-Webhook-Signature"],
        timestamp=request.headers["X-Webhook-Timestamp"],
        secret="your_webhook_secret",
        tolerance=300,                    # seconds (default)
    )
    # Signature is valid
except WebhookSignatureVerificationFailed as e:
    # Signature invalid or timestamp expired
    print(e)
```

## Error Handling

```python
from jetemail import JetEmail, SendEmailOptions, JetEmailError

client = JetEmail(api_key="your_api_key")

try:
    client.emails.send(
        SendEmailOptions(
            from_="you@yourdomain.com",
            to="recipient@example.com",
            subject="Test",
            html="<p>Hi</p>",
        )
    )
except JetEmailError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Response: {e.response}")
```

## License

MIT
