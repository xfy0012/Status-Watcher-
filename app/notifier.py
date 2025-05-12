import requests     # Used to send HTTP requests
import os   # Used to access environment variables
from dotenv import load_dotenv  # Loads environment variables from a .env file

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
        response = requests.post(DISCORD_WEBHOOK_URL, json = data)

        # Discord returns 204 No Content if the message is successfully sent
        if response.status_code == 204:
            print("Discord notification is sent")
        else:
            print(f"Discord notification send fail : {response.status_code}, {response.text}")
    except Exception as e:
        # Print error message if the request fails
        print(f"Discord send erro: {e}")


