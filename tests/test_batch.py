import pytest

from jetemail import SendEmailOptions
from tests.conftest import make_client_with_mock


class TestBatch:
    def test_send_batch(self):
        client = make_client_with_mock(
            {
                "summary": {"total": 2, "successful": 2, "failed": 0},
                "results": [
                    {"id": "msg_1", "response": "Queued"},
                    {"id": "msg_2", "response": "Queued"},
                ],
            }
        )

        emails = [
            SendEmailOptions(
                from_="sender@example.com",
                to="a@example.com",
                subject="Test 1",
                html="<p>1</p>",
            ),
            SendEmailOptions(
                from_="sender@example.com",
                to="b@example.com",
                subject="Test 2",
                text="2",
            ),
        ]

        result = client.batch.send(emails)
        assert result["summary"]["total"] == 2
        assert len(result["results"]) == 2

    def test_send_empty_batch_raises(self):
        client = make_client_with_mock({})

        with pytest.raises(ValueError, match="At least one email"):
            client.batch.send([])

    def test_send_over_100_raises(self):
        client = make_client_with_mock({})

        emails = [
            SendEmailOptions(
                from_="sender@example.com",
                to="a@example.com",
                subject="Test",
                html="<p>Hi</p>",
            )
            for _ in range(101)
        ]

        with pytest.raises(ValueError, match="100"):
            client.batch.send(emails)

    def test_send_batch_invalid_email_raises(self):
        client = make_client_with_mock({})

        emails = [
            SendEmailOptions(
                from_="sender@example.com",
                to="a@example.com",
                subject="Valid",
                html="<p>Hi</p>",
            ),
            SendEmailOptions(
                from_="",
                to="b@example.com",
                subject="Invalid",
                html="<p>Hi</p>",
            ),
        ]

        with pytest.raises(ValueError, match="index 1"):
            client.batch.send(emails)
