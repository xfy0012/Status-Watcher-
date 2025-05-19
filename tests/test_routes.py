
from app.models import Website

def test_add_website_success(client, db):
    """
    Test: Successfully add a website
    """
    response = client.post("/api/websites", json={"url": "https://example.com"})
    assert response.status_code == 201
    assert response.get_json()["message"] == "Website added"

    site = Website.query.filter_by(url="https://example.com").first()
    assert site is not None
    assert site.status == "unknown"
    assert site.user_id == 1

def test_add_website_missing_url(client):
    """
    Test: Add website with missing URL, should return 400
    """
    response = client.post("/api/websites", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_get_websites(client, db):
    """
    Test: Get website list
    """
    # Add test data
    db.session.add(Website(url="https://test.com", status="200", user_id=1))
    db.session.commit()

    response = client.get("/api/websites")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["url"] == "https://test.com"

def test_update_website_success(client, db):
    """
    Test: Successfully update website URL
    """
    site = Website(url="https://old.com", status="unknown", user_id=1)
    db.session.add(site)
    db.session.commit()

    response = client.put(f"/api/websites/{site.id}", json={"url": "https://new.com"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Website updated"

    updated = Website.query.get(site.id)
    assert updated.url == "https://new.com"

def test_update_website_not_found(client,db):
    """
    Test: Update a non-existent website, should return 404
    """
    response = client.put("/api/websites/9999", json={"url": "https://shouldfail.com"})
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_delete_website_success(client, db):
    """
    Test: Successfully delete a website
    """
    site = Website(url="https://tobedeleted.com", status="unknown", user_id=1)
    db.session.add(site)
    db.session.commit()

    response = client.delete(f"/api/websites/{site.id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Website deleted"

    deleted = Website.query.get(site.id)
    assert deleted is None

def test_delete_website_not_found(client, db):
    """
    Test: Delete a non-existent website
    """
    response = client.delete("/api/websites/9999")
    assert response.status_code == 404
    assert "error" in response.get_json()
