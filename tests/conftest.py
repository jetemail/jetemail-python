from jetemail import JetEmail


def make_mock_request(response_data):
    """Create a mock request function that returns the given data."""

    def mock_request(endpoint, body):
        return response_data

    return mock_request


def make_client_with_mock(response_data):
    """Create a JetEmail client with a mocked request function."""
    client = JetEmail.__new__(JetEmail)
    client._api_key = "test_key"
    client._base_url = "https://api.jetemail.com"
    client._request = make_mock_request(response_data)

    from jetemail.emails import Emails
    from jetemail.batch import Batch

    client.emails = Emails(client._request)
    client.batch = Batch(client._request)
    return client
