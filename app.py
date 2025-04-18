import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

# Načítanie premenných z .env
load_dotenv()

app = Flask(__name__)

# Získanie premenných z .env
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    if request.method == "POST":
        min_battles = request.form.get("min_battles", type=int)
        min_wtr = request.form.get("min_wtr", type=int)
        country = request.form.get("country")
        webhook_url = request.form.get("webhook_url") or DISCORD_WEBHOOK_URL

        # Získanie hráčov bez klanu
        players = get_players_without_clan(min_battles, min_wtr, country)

        if players:
            send_discord_notification(players, webhook_url)

    return render_template("index.html", players=players)

def get_players_without_clan(min_battles, min_wtr, country):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&search=&limit=100"
    response = requests.get(url)

    filtered_players = []

    if response.status_code == 200:
        data = response.json()
        for player in data.get("data", []):
            account_id = player.get("account_id")
            nickname = player.get("nickname")

            # Získaj podrobné štatistiky pre hráča
            info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}"
            info_response = requests.get(info_url)
            if info_response.status_code != 200:
                continue

            info_data = info_response.json().get("data", {}).get(str(account_id), {})
            statistics = info_data.get("statistics", {}).get("all", {})
            battles = statistics.get("battles", 0)
            wtr = info_data.get("global_rating", 0)
            clan_id = info_data.get("clan_id")
            last_battle_time = info_data.get("last_battle_time", 0)

            # Filter
            if clan_id is None and battles >= min_battles and wtr >= min_wtr:
                if country == "any" or info_data.get("client_language", "").lower() == country.lower():
                    filtered_players.append({
                        "nickname": nickname,
                        "battles": battles,
                        "wtr": wtr,
                        "last_battle": last_battle_time
                    })
    return filtered_players

def send_discord_notification(players, webhook_url):
    for player in players:
        message = (
            f"**Nový hráč bez klanu!**\n"
            f"Prezývka: {player['nickname']}\n"
            f"Bitky: {player['battles']}\n"
            f"WTR: {player['wtr']}\n"
            f"Posledná bitka: {player['last_battle']}"
        )
        payload = {"content": message}
        requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
