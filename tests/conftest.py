import pytest
from app import create_app, db as _db

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use in-memory SQLite for testing
        "SCHEDULER_API_ENABLED": False
    })
    with app.app_context():
        yield app

@pytest.fixture(scope="function")
def db(app):
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
