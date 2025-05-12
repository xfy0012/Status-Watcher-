from app import db  # Import the SQLAlchemy database instance
from datetime import datetime

# User model representing each account in the system
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    websites = db.relationship('Website', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

# Website model representing a monitored website
class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='unknown')
    check_interval = db.Column(db.Integer, default=300)
    last_checked = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    history = db.relationship('StatusHistory', backref='website', lazy=True)

# StatusHistory model to log past status checks for a website
class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    response_time = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)

# Notification model to store user notification configurations (e.g., Discord webhook, email)
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    config = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)