# Purpose: This test file verifies the functionality of the routes module, particularly the `/` route.
# It ensures that:
# 1. The home route is accessible.
# 2. The response contains the expected content.

import unittest
from app import create_app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Create a test instance of the Flask application
        self.app = create_app()
        self.app.testing = True  # Enable testing mode
        self.client = self.app.test_client()  # Create a test client for making requests

    def test_home_route(self):
        # Send a GET request to the home route ('/')
        response = self.client.get('/')
        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Assert that the response contains the expected content ('Status Watcher')
        self.assertIn(b'Status Watcher', response.data)
