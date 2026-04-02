import pytest

from jetemail import SendEmailOptions, Attachment
from tests.conftest import make_client_with_mock


class TestEmails:
    def test_send_with_html(self):
        client = make_client_with_mock({"id": "msg_123", "response": "Queued"})

        result = client.emails.send(
            SendEmailOptions(
                from_="sender@example.com",
                to="recipient@example.com",
                subject="Test",
                html="<p>Hello</p>",
            )
        )

        assert result["id"] == "msg_123"

    def test_send_with_text(self):
        client = make_client_with_mock({"id": "msg_456", "response": "Queued"})

        result = client.emails.send(
            SendEmailOptions(
                from_="sender@example.com",
                to="recipient@example.com",
                subject="Test",
                text="Hello",
            )
        )

        assert result["id"] == "msg_456"

    def test_send_with_multiple_recipients(self):
        client = make_client_with_mock({"id": "msg_789", "response": "Queued"})

        result = client.emails.send(
            SendEmailOptions(
                from_="sender@example.com",
                to=["a@example.com", "b@example.com"],
                subject="Test",
                html="<p>Hi</p>",
            )
        )

        assert result["id"] == "msg_789"

    def test_send_with_all_options(self):
        client = make_client_with_mock({"id": "msg_full", "response": "Queued"})

        result = client.emails.send(
            SendEmailOptions(
                from_="sender@example.com",
                to="recipient@example.com",
                subject="Full test",
                html="<p>Hello</p>",
                text="Hello",
                cc="cc@example.com",
                bcc=["bcc1@example.com", "bcc2@example.com"],
                reply_to="reply@example.com",
                headers={"X-Custom": "value"},
                attachments=[
                    Attachment.from_content("file content", "test.txt")
                ],
            )
        )

        assert result["id"] == "msg_full"

    def test_send_missing_from_raises(self):
        client = make_client_with_mock({})

        with pytest.raises(ValueError, match="from_"):
            client.emails.send(
                SendEmailOptions(
                    from_="",
                    to="recipient@example.com",
                    subject="Test",
                    html="<p>Hi</p>",
                )
            )

    def test_send_missing_to_raises(self):
        client = make_client_with_mock({})

        with pytest.raises(ValueError, match="to"):
            client.emails.send(
                SendEmailOptions(
                    from_="sender@example.com",
                    to="",
                    subject="Test",
                    html="<p>Hi</p>",
                )
            )

    def test_send_missing_subject_raises(self):
        client = make_client_with_mock({})

        with pytest.raises(ValueError, match="subject"):
            client.emails.send(
                SendEmailOptions(
                    from_="sender@example.com",
                    to="recipient@example.com",
                    subject="",
                    html="<p>Hi</p>",
                )
            )

    def test_send_missing_body_raises(self):
        client = make_client_with_mock({})

        with pytest.raises(ValueError, match="html.*text"):
            client.emails.send(
                SendEmailOptions(
                    from_="sender@example.com",
                    to="recipient@example.com",
                    subject="Test",
                )
            )


class TestSendEmailOptions:
    def test_to_dict_minimal(self):
        options = SendEmailOptions(
            from_="sender@example.com",
            to="recipient@example.com",
            subject="Test",
            html="<p>Hi</p>",
        )
        d = options.to_dict()

        assert d["from"] == "sender@example.com"
        assert d["to"] == "recipient@example.com"
        assert d["subject"] == "Test"
        assert d["html"] == "<p>Hi</p>"
        assert "text" not in d
        assert "cc" not in d
        assert "bcc" not in d
        assert "reply_to" not in d
        assert "headers" not in d
        assert "attachments" not in d

    def test_to_dict_full(self):
        options = SendEmailOptions(
            from_="sender@example.com",
            to=["a@example.com", "b@example.com"],
            subject="Test",
            html="<p>Hi</p>",
            text="Hi",
            cc="cc@example.com",
            bcc="bcc@example.com",
            reply_to="reply@example.com",
            headers={"X-Custom": "value"},
            attachments=[Attachment(filename="f.txt", data="YWJj")],
        )
        d = options.to_dict()

        assert d["cc"] == "cc@example.com"
        assert d["reply_to"] == "reply@example.com"
        assert d["headers"] == {"X-Custom": "value"}
        assert d["attachments"] == [{"filename": "f.txt", "data": "YWJj"}]
