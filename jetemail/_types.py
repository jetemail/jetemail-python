import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class Attachment:
    """An email attachment with base64-encoded data."""

    filename: str
    data: str

    @staticmethod
    def from_path(path: str, filename: Optional[str] = None) -> "Attachment":
        """Create an attachment from a file path."""
        with open(path, "rb") as f:
            content = f.read()
        return Attachment(
            filename=filename or os.path.basename(path),
            data=base64.b64encode(content).decode("ascii"),
        )

    @staticmethod
    def from_content(content: Union[str, bytes], filename: str) -> "Attachment":
        """Create an attachment from raw content."""
        if isinstance(content, str):
            content = content.encode("utf-8")
        return Attachment(
            filename=filename,
            data=base64.b64encode(content).decode("ascii"),
        )

    def to_dict(self) -> Dict[str, str]:
        return {"filename": self.filename, "data": self.data}


@dataclass
class SendEmailOptions:
    """Options for sending an email via the JetEmail API."""

    from_: str
    to: Union[str, List[str]]
    subject: str
    html: Optional[str] = None
    text: Optional[str] = None
    cc: Optional[Union[str, List[str]]] = None
    bcc: Optional[Union[str, List[str]]] = None
    reply_to: Optional[Union[str, List[str]]] = None
    headers: Optional[Dict[str, str]] = None
    attachments: Optional[List[Attachment]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to API payload. Only includes non-None optional fields."""
        payload: Dict[str, Any] = {
            "from": self.from_,
            "to": self.to,
            "subject": self.subject,
        }

        if self.html is not None:
            payload["html"] = self.html
        if self.text is not None:
            payload["text"] = self.text
        if self.cc is not None:
            payload["cc"] = self.cc
        if self.bcc is not None:
            payload["bcc"] = self.bcc
        if self.reply_to is not None:
            payload["reply_to"] = self.reply_to
        if self.headers is not None:
            payload["headers"] = self.headers
        if self.attachments is not None:
            payload["attachments"] = [a.to_dict() for a in self.attachments]

        return payload
