from flask_sqlalchemy import SQLAlchemy     # Import SQLAlchemy for ORM (Object Relational Mapping)
from flask_apscheduler import APScheduler   # Import APScheduler to enable scheduled background tasks

# Initialize a SQLAlchemy database instance
db = SQLAlchemy()

# Initialize an APScheduler instance for periodic jobs
scheduler = APScheduler()
