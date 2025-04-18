import requests

def send_discord_notification(players, webhook_url):
    if not webhook_url:
        return

    for player in players:
        message = (
            f"**🔍 Nový hráč bez klanu nájdený:**\n"
            f"👤 Prezývka: {player['nickname']}\n"
            f"🎯 WTR: {player['wtr']}\n"
            f"🕹️ Bitky: {player['battles']}\n"
            f"🌍 Krajina: {player['country']}\n"
            f"https://worldoftanks.eu/en/community/accounts/{player['account_id']}/"
        )
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)

        if response.status_code not in [200, 204]:
            print(f"❌ Chyba pri posielaní na Discord: {response.status_code} - {response.text}")
