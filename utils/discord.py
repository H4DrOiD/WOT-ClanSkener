import requests

def send_discord_notification(webhook_url, players):
    if not players:
        return

    content = "**🎯 Noví hráči bez klanu, ktorí spĺňajú tvoje kritériá:**\n"
    for player in players:
        content += f"🔹 **{player['nickname']}** – {player['battles']} hier, WTR: {player['wtr']}, Krajina: {player['country']}\n"

    payload = {
        "content": content
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Chyba pri odosielaní webhooku: {e}")
