from typing import Any, Callable, Dict, List

from ._types import SendEmailOptions
from .emails import Emails


class Batch:
    """Send batch emails via the JetEmail API."""

    def __init__(self, request: Callable[[str, Dict[str, Any]], Dict[str, Any]]):
        self._request = request
        self._email_validator = Emails(request)

    def send(self, emails: List[SendEmailOptions]) -> Dict[str, Any]:
        """Send a batch of emails (1-100).

        Args:
            emails: A list of SendEmailOptions instances.

        Returns:
            API response dict with 'summary' and 'results'.

        Raises:
            ValueError: If the batch is empty, exceeds 100, or any email is invalid.
            JetEmailError: If the API request fails.
        """
        if not emails:
            raise ValueError("At least one email is required.")
        if len(emails) > 100:
            raise ValueError("A maximum of 100 emails can be sent per batch.")

        for i, email in enumerate(emails):
            try:
                self._email_validator._validate(email)
            except ValueError as e:
                raise ValueError(f"Email at index {i}: {e}") from e

        body = {"emails": [email.to_dict() for email in emails]}
        return self._request("/email-batch", body)
