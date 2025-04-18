import os
import requests
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    error = None

    if request.method == "POST":
        try:
            min_battles = int(request.form.get("min_battles", 0))
            min_wtr = int(request.form.get("min_wtr", 0))
            country = request.form.get("country", "any")
            webhook_url = request.form.get("webhook")

            if not webhook_url:
                error = "Zadaj Discord webhook!"
                return render_template("index.html", players=[], error=error)

            # zavolaj funkciu na získanie hráčov
            players = get_players(min_battles, min_wtr, country)

            if players:
                send_to_discord(players, webhook_url)

        except Exception as e:
            error = f"Nastala chyba: {str(e)}"

    return render_template("index.html", players=players, error=error)

def get_players(min_battles, min_wtr, country):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100"
    response = requests.get(url)
    filtered_players = []

    if response.status_code == 200:
        for player in response.json().get("data", []):
            account_id = player.get("account_id")
            nickname = player.get("nickname")

            if not account_id:
                continue

            info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=statistics"
            info_res = requests.get(info_url).json()
            info = info_res.get("data", {}).get(str(account_id), {})

            if info and not info.get("clan_id"):
                battles = info.get("statistics", {}).get("all", {}).get("battles", 0)
                wtr = info.get("global_rating", 0)
                last_battle = info.get("last_battle_time")
                country_code = info.get("client_language", "")

                if (
                    battles >= min_battles
                    and wtr >= min_wtr
                    and (country == "any" or country_code.lower() == country.lower())
                ):
                    filtered_players.append({
                        "nickname": nickname,
                        "battles": battles,
                        "wtr": wtr,
                        "country": country_code,
                        "last_battle": datetime.utcfromtimestamp(last_battle).strftime('%d.%m.%Y %H:%M') if last_battle else "neznámy",
                        "account_id": account_id
                    })
    return filtered_players

def send_to_discord(players, webhook_url):
    for player in players:
        msg = f"**Hráč bez klanu nájdený!**\n"
        msg += f"Prezývka: {player['nickname']}\n"
        msg += f"Bitky: {player['battles']}\n"
        msg += f"WTR: {player['wtr']}\n"
        msg += f"Krajina: {player['country']}\n"
        msg += f"Posledná bitka: {player['last_battle']}\n"
        msg += f"https://worldoftanks.eu/ltw/user/{player['account_id']}"

        requests.post(webhook_url, json={"content": msg})

if __name__ == "__main__":
    app.run(debug=True)
