import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    if request.method == "POST":
        min_battles = int(request.form.get("min_battles", 0))
        min_wtr = int(request.form.get("min_wtr", 0))
        country = request.form.get("country")
        webhook_url = request.form.get("webhook_url")

        players = get_unclanned_players(min_battles, min_wtr, country)

        if players and webhook_url:
            notify_discord(players, webhook_url)

    return render_template("index.html", players=players)

def get_unclanned_players(min_battles, min_wtr, country):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&search=&limit=100"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json().get("data", [])
    result = []

    for player in data:
        account_id = player["account_id"]
        nickname = player["nickname"]

        details = get_player_details(account_id)
        if not details:
            continue

        stats = details.get("statistics", {}).get("all", {})
        battles = stats.get("battles", 0)
        wtr = details.get("global_rating", 0)
        clan = details.get("clan", None)
        last_battle_time = details.get("last_battle_time", 0)
        account_level = details.get("account_leveling", {}).get("level", 0)
        player_country = details.get("country", "")

        if (
            battles >= min_battles and
            wtr >= min_wtr and
            clan is None and
            (country == "any" or country == player_country)
        ):
            result.append({
                "nickname": nickname,
                "battles": battles,
                "wtr": wtr,
                "last_battle": last_battle_time,
                "level": account_level,
                "country": player_country
            })

    return result

def get_player_details(account_id):
    url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=global_rating"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["data"].get(str(account_id), {})
    return {}

def notify_discord(players, webhook_url):
    for player in players:
        message = (
            f"🕵️ Nový hráč bez klanu:\n"
            f"👤 Nick: {player['nickname']}\n"
            f"🎯 Bitky: {player['battles']}\n"
            f"🏆 WTR: {player['wtr']}\n"
            f"🌍 Krajina: {player['country']}\n"
        )
        requests.post(webhook_url, json={"content": message})

if __name__ == "__main__":
    app.run(debug=True)
