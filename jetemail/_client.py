from .batch import Batch
from ._http_client import create_request_fn
from .emails import Emails
from .exceptions import ApiKeyIsMissing


class JetEmail:
    """JetEmail API client for sending transactional emails.

    Usage:
        client = JetEmail(api_key="your_api_key")
        client.emails.send(SendEmailOptions(...))
        client.batch.send([SendEmailOptions(...), ...])
    """

    def __init__(
        self, api_key: str = "", base_url: str = "https://api.jetemail.com"
    ):
        if not api_key:
            raise ApiKeyIsMissing()

        self._api_key = api_key
        self._base_url = base_url
        self._request = create_request_fn(api_key, base_url)

        self.emails = Emails(self._request)
        self.batch = Batch(self._request)
