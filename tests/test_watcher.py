# tests/test_watcher.py
from app.models import Website
from app.watcher import check_all_websites
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

@patch("app.watcher.httpx.get")
@patch("app.watcher.send_status_to_discord")
@patch("app.watcher.status_code_gauge")
@patch("app.watcher.response_time_gauge")
@patch("app.watcher.status_change_counter")
def test_website_status_change_triggers_discord(
    mock_counter,
    mock_response_gauge,
    mock_code_gauge,
    mock_send_discord,
    mock_httpx_get,
    db,
    app
):
    """
    Purpose:
    Verify that when a website status changes from 'down' to '200':
    - The status is updated
    - The Discord notification function is called
    - The last_checked field is updated
    """
    # Arrange: Create a website instance and add it to the database
    with app.app_context():
        site = Website(url="https://example.com", 
                       status="down", 
                       user_id=1,
                       last_checked=datetime.utcnow() - timedelta(minutes=5))
        db.session.add(site)
        db.session.commit()

    # Mock httpx to return 200
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_httpx_get.return_value = mock_response

    # Act: Run the status check
    check_all_websites(app)

    # Assert: Check that status changed and notification was sent
    with app.app_context():
        updated_site = Website.query.filter_by(url="https://example.com").first()
        assert updated_site.status == "200"
        assert updated_site.last_checked is not None
        mock_send_discord.assert_called_once_with("https://example.com", "200")
