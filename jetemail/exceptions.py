from typing import Any, Dict, Optional


class JetEmailError(Exception):
    """Base exception for JetEmail API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 0,
        response: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(message)


class ApiKeyIsMissing(Exception):
    """Raised when no API key is provided."""

    def __init__(self) -> None:
        super().__init__(
            "The JetEmail API key is missing. "
            "Pass it to the JetEmail constructor: JetEmail(api_key='...')"
        )
