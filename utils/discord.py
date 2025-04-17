import requests

def send_discord_notification(webhook_url, message):
    """Pošle správu na zadaný Discord webhook."""
    data = {
        "content": message
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"❌ Chyba pri odosielaní na Discord: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Výnimka pri odosielaní na Discord: {e}")
