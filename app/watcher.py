from app.models import Website
from app.tool import db, scheduler
import httpx
from datetime import datetime
from flask import current_app
from app.notifier import send_status_to_discord
from prometheus_client import Gauge, Counter

# Prometheus metric: HTTP status code per website
status_code_gauge = Gauge("website_status_code", "HTTP status code", ["url"])

# Prometheus metric: Response time in seconds per website
response_time_gauge = Gauge("website_response_time_seconds", "HTTP response time in seconds", ["url"])

# Prometheus metric: Count of status changes per website
status_change_counter = Counter("website_status_change_total", "Number of status changes", ["url"])


# Function to check the status of all websites in the database
def check_all_websites(app):
    with app.app_context():     # Ensure we're within Flask's application context
        print("Running the website checks...")
        websites = Website.query.all()
        for site in websites:
            print(f"checking {site.url}")
            try:

                start = datetime.now()  # Record start time for response time calculation
                response = httpx.get(site.url, timeout=5)   # Attempt to make a GET request to the website
                duration = (datetime.now() - start).total_seconds()  # Calculate response time

                new_status = str(response.status_code)  # Save status code as string

                response_time_gauge.labels(url=site.url).set(duration)
                status_code_gauge.labels(url=site.url).set(int(response.status_code))
            except httpx.TimeoutException:
                # Handle timeout specifically
                new_status = "timeout"
                response_time_gauge.labels(url=site.url).set(0)
                status_code_gauge.labels(url=site.url).set(0)
                print(f"Timeout when checking {site.url}")
            except httpx.RequestError:
                # Handle network-related errors (DNS failure, refused connection, etc.)
                new_status = "unreachable"
                response_time_gauge.labels(url=site.url).set(0)
                status_code_gauge.labels(url=site.url).set(0)
                print(f"Request error when checking {site.url}")
            except Exception as e:
                # Handle all other exceptions as generic 'down' status
                new_status = "down"
                response_time_gauge.labels(url=site.url).set(0)
                status_code_gauge.labels(url=site.url).set(0)
                print(f"Unknown error when checking {site.url}: {e}")

            if site.status != new_status:
                send_status_to_discord(site.url, new_status)
                print(f"{site.url} status change: {site.status} → {new_status}")
                status_change_counter.labels(url=site.url).inc()
                site.status = new_status

            site.last_checked = datetime.now()
            
        db.session.commit()

def setup_jobs(app):
    with app.app_context():
        scheduler.add_job(
            id='check_websites',
            func= lambda : check_all_websites(app),
            trigger = 'interval',
            seconds = 30
        )
        scheduler.start()

