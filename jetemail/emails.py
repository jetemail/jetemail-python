from typing import Any, Callable, Dict

from ._types import SendEmailOptions


class Emails:
    """Send single emails via the JetEmail API."""

    def __init__(self, request: Callable[[str, Dict[str, Any]], Dict[str, Any]]):
        self._request = request

    def send(self, options: SendEmailOptions) -> Dict[str, Any]:
        """Send a single email.

        Args:
            options: A SendEmailOptions instance with the email details.

        Returns:
            API response dict containing 'id' and 'response'.

        Raises:
            ValueError: If required fields are missing or invalid.
            JetEmailError: If the API request fails.
        """
        self._validate(options)
        return self._request("/email", options.to_dict())

    def _validate(self, options: SendEmailOptions) -> None:
        if not options.from_:
            raise ValueError("The 'from_' field is required.")
        if not options.to:
            raise ValueError("The 'to' field is required.")
        if not options.subject:
            raise ValueError("The 'subject' field is required.")
        if not options.html and not options.text:
            raise ValueError("At least one of 'html' or 'text' is required.")
