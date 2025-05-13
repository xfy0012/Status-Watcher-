from app.models import Website
from app.tool import db, scheduler
import httpx
from datetime import datetime
from flask import current_app
from app.notifier import send_status_to_discord
from prometheus_client import Gauge, Counter
import logging

# Prometheus metric: HTTP status code per website
status_code_gauge = Gauge("website_status_code", "HTTP status code", ["url"])

# Prometheus metric: Response time in seconds per website
response_time_gauge = Gauge("website_response_time_seconds", "HTTP response time in seconds", ["url"])

# Prometheus metric: Count of status changes per website
status_change_counter = Counter("website_status_change_total", "Number of status changes", ["url"])

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to check the status of all websites in the database
def check_all_websites(app):
    with app.app_context():
        logging.info("Starting website checks...")
        websites = Website.query.all()
        for site in websites:
            try:
                start = datetime.now()
                response = httpx.get(site.url, timeout=current_app.config['HTTP_TIMEOUT'])
                duration = (datetime.now() - start).total_seconds()

                new_status = str(response.status_code)

                # Update Prometheus metrics
                response_time_gauge.labels(url=site.url).set(duration)
                status_code_gauge.labels(url=site.url).set(int(response.status_code))

            except Exception as e:
                logging.error(f"Error checking {site.url}: {e}")
                new_status = "down"
                response_time_gauge.labels(url=site.url).set(0)
                status_code_gauge.labels(url=site.url).set(0)

            if site.status != new_status:
                logging.info(f"{site.url} status change: {site.status} → {new_status}")
                send_status_to_discord(site.url, new_status)
                status_change_counter.labels(url=site.url).inc()
                site.status = new_status

            site.last_checked = datetime.now()

        db.session.commit()
        logging.info("Website checks completed.")

def setup_jobs(app):
    with app.app_context():
        scheduler.add_job(
            id='check_websites',
            func= lambda : check_all_websites(app),
            trigger = 'interval',
            seconds = 30
        )
        scheduler.start()

