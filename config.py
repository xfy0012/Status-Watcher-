import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/sites.db')
    HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', 10))
    SCHEDULER_INTERVAL = int(os.getenv('SCHEDULER_INTERVAL', 30))

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')  # Ensure this is set in production
    DEBUG = False