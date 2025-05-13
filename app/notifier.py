import httpx     # Used to send HTTP requests
import os   # Used to access environment variables
from dotenv import load_dotenv  # Loads environment variables from a .env file
import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file into the environment
load_dotenv()

# Get the Discord webhook URL from the environment
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Function to send a website status message to a Discord channel
def send_status_to_discord(website_url, status):
    content = f" website alert `{website_url}` status: {status.upper()}"
    data = {"content" : content}
    

    try:
         # Send POST request to Discord webhook
        response = httpx.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)

        # Discord returns 204 No Content if the message is successfully sent
        if response.status_code == 204:
            logging.info("Discord notification sent.")
        else:
            logging.warning(f"Discord notification failed: {response.status_code}, {response.text}")
    except Exception as e:
        # Log any exceptions that occur during the request
        logging.error(f"Discord send error: {e}")

    
    