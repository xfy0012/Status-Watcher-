# Purpose: This test file verifies the functionality of the `check_all_websites` function in the `watcher` module.
# It ensures that:
# 1. HTTP requests to websites are handled correctly.
# 2. Website statuses are updated in the database as expected.
# 3. Notifications are sent for status changes.

import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.models import Website, User
from app.tool import db
from app.watcher import check_all_websites


class TestWatcher(unittest.TestCase):

    def setUp(self):
        # Set up a Flask application with an in-memory SQLite database for testing
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['HTTP_TIMEOUT'] = 10  # Set HTTP timeout for testing
        self.app.app_context().push()
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()  # Create all database tables

            # Add a test user to the database
            user = User(email='test@example.com', password_hash='dummy')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id  # Store the user ID for later use

            # Add test websites to the database
            db.session.add_all([
                Website(url='https://example.com', status='200', user_id=self.user_id),  # Valid website
                Website(url='https://nonexistent.com', status='down', user_id=self.user_id)  # Invalid website
            ])
            db.session.commit()

    def tearDown(self):
        # Clean up the database after each test
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('app.watcher.send_status_to_discord')
    @patch('app.watcher.httpx.get')
    def test_check_all_websites(self, mock_httpx_get, mock_send_status_to_discord):
        # Mock HTTP responses for the websites
        mock_httpx_get.side_effect = [
            MagicMock(status_code=500),  # Simulate a failed response for the first website
            MagicMock(status_code=200)   # Simulate a successful response for the second website
        ]

        with self.app.app_context():
            # Set initial statuses to ensure a state change occurs
            site1 = Website.query.filter_by(url='https://example.com').first()
            site2 = Website.query.filter_by(url='https://nonexistent.com').first()
            site1.status = '200'  # Initial status is '200'
            site2.status = 'down'  # Initial status is 'down'
            db.session.commit()

            # Call the function to check all websites
            check_all_websites(self.app)

            # Fetch the updated website records from the database
            site1 = Website.query.filter_by(url='https://example.com').first()
            site2 = Website.query.filter_by(url='https://nonexistent.com').first()

            # Assert that the status of the first website is updated to '500'
            self.assertEqual(site1.status, '500')

            # Assert that the status of the second website is updated to '200'
            self.assertEqual(site2.status, '200')

            # Verify that notifications were sent for both websites
            mock_send_status_to_discord.assert_any_call('https://example.com', '500')
            mock_send_status_to_discord.assert_any_call('https://nonexistent.com', '200')
            self.assertEqual(mock_send_status_to_discord.call_count, 2)
