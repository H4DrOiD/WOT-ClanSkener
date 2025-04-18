import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    error = None

    if request.method == "POST":
        try:
            min_battles = int(request.form.get("min_battles", 0))
            min_wtr = int(request.form.get("min_wtr", 0))
            country = request.form.get("country", "").upper()
            webhook = request.form.get("webhook", "")

            players = get_unclanned_players(min_battles, min_wtr, country)

            if players and webhook:
                send_to_discord(players, webhook)

        except Exception as e:
            error = str(e)

    return render_template("index.html", players=players, error=error)

def get_unclanned_players(min_battles, min_wtr, country):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100&type=all"
    response = requests.get(url)
    players = []

    if response.status_code == 200:
        data = response.json().get("data", [])
        for player in data:
            account_id = player["account_id"]
            nickname = player["nickname"]

            info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=statistics"
            info_resp = requests.get(info_url)
            info_data = info_resp.json()["data"].get(str(account_id), {})

            if not info_data:
                continue

            battles = info_data.get("statistics", {}).get("all", {}).get("battles", 0)
            wtr = info_data.get("global_rating", 0)
            clan_id = info_data.get("clan_id", None)
            country_code = info_data.get("client_language", "").upper()

            if (clan_id is None and
                battles >= min_battles and
                wtr >= min_wtr and
                (country == "" or country == country_code)):
                players.append({
                    "nickname": nickname,
                    "battles": battles,
                    "wtr": wtr,
                    "country": country_code,
                    "profile_link": f"https://worldoftanks.eu/en/community/accounts/{account_id}/"
                })

    return players

def send_to_discord(players, webhook_url):
    for player in players:
        message = (
            f"**Hráč bez klanu:**\n"
            f"👤 {player['nickname']}\n"
            f"🎯 WTR: {player['wtr']}\n"
            f"⚔️ Bitky: {player['battles']}\n"
            f"🌍 Krajina: {player['country']}\n"
            f"🔗 [Profil]({player['profile_link']})"
        )
        payload = {"content": message}
        requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
