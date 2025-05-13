# Purpose: This test file verifies the functionality of the `send_status_to_discord` function in the `notifier` module.
# It ensures that:
# 1. Notifications are sent to Discord with the correct payload.
# 2. The function handles HTTP responses as expected.

import unittest
from unittest.mock import patch


class TestNotifier(unittest.TestCase):

    @patch('app.notifier.httpx.post')
    def test_send_status_to_discord(self, mock_post):
        from app.notifier import send_status_to_discord

        # Mock the HTTP POST response to simulate a successful notification
        mock_post.return_value.status_code = 204

        # Call the function with test data
        send_status_to_discord('https://example.com', 'down')

        # Verify that the HTTP POST request was made with the correct arguments
        mock_post.assert_called_once_with(
            'https://discord.com/api/webhooks/your_webhook_here',
            json={'content': ' website alert `https://example.com` status: DOWN'},
            timeout=10
        )
