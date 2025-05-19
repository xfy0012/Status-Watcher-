# App Folder Overview

This folder contains the core logic of the Status Watcher application, a Flask-based web app for monitoring website uptime, sending notifications, and providing a web interface for management.

---

## Key Components

### 1. `__init__.py`
- Initializes the Flask application and its extensions (SQLAlchemy, APScheduler, Flask-Migrate).
- Loads configuration from `config.py` and instance config.
- Registers the `main` blueprint for API and web routes.
- Sets up periodic jobs for website monitoring using `setup_jobs`.
- Defines the home route (`/`) to render the main HTML page (`index.html`).

### 2. `models.py`
- Defines the database models using SQLAlchemy:
  - **`User`**: Represents a user with email and password.
  - **`Website`**: Represents a monitored website with fields like `url`, `status`, `last_checked`, and `user_id`.
  - **`StatusHistory`**: Logs past status checks for a website.
  - **`Notification`**: Stores user notification configurations (e.g., Discord webhook).

### 3. `routes.py`
- Implements API endpoints for managing websites:
  - `GET /api/websites`: Fetches all monitored websites.
  - `POST /api/websites`: Adds a new website to monitor.
  - `PUT /api/websites/<id>`: Updates an existing website.
  - `DELETE /api/websites/<id>`: Deletes a website.
- All API endpoints interact with the `Website` model and return JSON responses.

### 4. `tool.py`
- Initializes shared tools:
  - **`db`**: SQLAlchemy instance for database operations.
  - **`scheduler`**: APScheduler instance for periodic tasks.

### 5. `watcher.py`
- Contains the core logic for monitoring websites:
  - **`check_all_websites`**: Checks the status of all websites in the database, updates their status, and sends notifications if the status changes.
  - **`setup_jobs`**: Configures a periodic job to run `check_all_websites` every 30 seconds.
- Integrates Prometheus metrics for observability:
  - Tracks HTTP status codes, response times, and status changes for each website.

### 6. `notifier.py`
- Handles sending notifications to Discord:
  - **`send_status_to_discord`**: Sends a POST request to a Discord webhook with the website's status.
  - Uses environment variables for webhook configuration.

---

## How It Works

1. **Initialization**
   - The application is initialized in `__init__.py` with configurations from `config.py` and instance config.
   - The database and scheduler are set up, and the `main` blueprint is registered.

2. **Website Monitoring**
   - The `check_all_websites` function in `watcher.py` is periodically executed by APScheduler.
   - It fetches all websites from the database, checks their status using HTTP requests, and updates the database.
   - If a website's status changes, a notification is sent via Discord.
   - Prometheus metrics are updated for each check.

3. **Web Interface**
   - The home route (`/`) serves the `index.html` template, which provides a user interface for managing websites.
   - The frontend interacts with the backend API (`routes.py`) to add, update, or delete websites.

4. **Notifications**
   - When a website's status changes, the `send_status_to_discord` function in `notifier.py` sends a notification to a configured Discord webhook.


