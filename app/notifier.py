import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_status_to_discord(website_url, status):
    content = f" website alert `{website_url}` status: {status.upper()}"
    data = {"content" : content}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json = data)
        if response.status_code == 204:
            print("Discord notification is sent")
        else:
            print(f"Discord notification send fail : {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Discord send erro: {e}")


