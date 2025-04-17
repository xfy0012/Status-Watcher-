from app.models import Website
from app.tool import db, scheduler
import httpx
from datetime import datetime
from flask import current_app
from app.notifier import send_status_to_discord
from prometheus_client import Gauge, Counter

#website code
status_code_gauge = Gauge("website_status_code", "HTTP status code", ["url"])
#Response Time
response_time_gauge = Gauge("website_response_time_seconds", "HTTP response time in seconds", ["url"])
#status change
status_change_counter = Counter("website_status_change_total", "Number of status changes", ["url"])


def check_all_websites(app):
    with app.app_context(): #get the flask app context
        print("Running the website checks...")
        websites = Website.query.all()
        for site in websites:
            print("checking{site.url}")
            try:
                start = datetime.now()
                response = httpx.get(site.url, timeout=5)
                duration = (datetime.now() - start).total_seconds()

                new_status = str(response.status_code)
                response_time_gauge.labels(url=site.url).set(duration)
                status_code_gauge.labels(url=site.url).set(int(response.status_code))

            except Exception as e:
                new_status = "down"
                response_time_gauge.labels(url=site.url).set(0)
                status_code_gauge.labels(url=site.url).set(0)

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

