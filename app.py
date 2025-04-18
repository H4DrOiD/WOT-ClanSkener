import os
import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []

    if request.method == "POST":
        min_battles = int(request.form.get("min_battles", 0))
        min_wtr = int(request.form.get("min_wtr", 0))
        country = request.form.get("country", "")
        webhook_url = request.form.get("webhook", "")

        search_url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100"

        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            for player_data in data.get("data", []):
                account_id = player_data["account_id"]
                nickname = player_data["nickname"]

                info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=statistics"
                info_response = requests.get(info_url)

                if info_response.status_code != 200:
                    continue

                info_data = info_response.json()["data"].get(str(account_id), {})

                if not info_data or info_data.get("clan_id"):
                    continue

                battles = info_data.get("statistics", {}).get("all", {}).get("battles", 0)
                last_battle_time = info_data.get("last_battle_time", 0)
                last_battle = datetime.utcfromtimestamp(last_battle_time).strftime('%d.%m.%Y %H:%M') if last_battle_time else "N/A"
                account_level = info_data.get("global_rating", "N/A")
                player_country = info_data.get("client_language", "N/A")

                if battles >= min_battles and account_level >= min_wtr and player_country.upper() == country.upper():
                    player = {
                        "account_id": account_id,
                        "nickname": nickname,
                        "battles": battles,
                        "last_battle": last_battle,
                        "account_level": account_level,
                        "country": player_country
                    }
                    players.append(player)

            # Poslať na Discord
            if webhook_url and players:
                send_discord_notification(webhook_url, players)

    return render_template("index.html", players=players)


def send_discord_notification(webhook_url, players):
    for player in players:
        msg = (
            f"**Hráč bez klanu nájdený:**\n"
            f"Prezývka: {player['nickname']}\n"
            f"Hry: {player['battles']}\n"
            f"WTR: {player['account_level']}\n"
            f"Posledná bitka: {player['last_battle']}\n"
            f"Krajina: {player['country']}\n"
            f"Profil: https://worldoftanks.eu/en/community/accounts/{player['account_id']}/"
        )
        payload = {"content": msg}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Chyba pri posielaní na Discord: {e}")


if __name__ == "__main__":
    app.run(debug=True)
