from typing import Any, Callable, Dict

import requests

from .exceptions import JetEmailError
from .version import __version__


def create_request_fn(
    api_key: str, base_url: str
) -> Callable[[str, Dict[str, Any]], Dict[str, Any]]:
    """Create a request function bound to the given API key and base URL."""

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"jetemail-python/{__version__}",
        }
    )

    def request(endpoint: str, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{base_url.rstrip('/')}{endpoint}"

        try:
            response = session.post(url, json=body)
        except requests.RequestException as e:
            raise JetEmailError(
                message=str(e),
                status_code=getattr(e.response, "status_code", 0) if e.response else 0,
            ) from e

        try:
            data = response.json() if response.content else {}
        except ValueError:
            data = {}

        if not response.ok:
            message = data.get("message") or data.get("error") or response.reason
            raise JetEmailError(
                message=message,
                status_code=response.status_code,
                response=data,
            )

        return data

    return request
