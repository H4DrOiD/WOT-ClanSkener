import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Získaj API kľúč z environment premennej alebo použije default
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    error = None

    if request.method == "POST":
        try:
            min_battles = int(request.form.get("min_battles", 0))
            min_wtr = int(request.form.get("min_wtr", 0))
            country = request.form.get("country", "")
            webhook_url = request.form.get("webhook", "").strip()

            # Získaj zoznam hráčov bez klanu cez Wargaming API
            players = get_unclanned_players(min_battles, min_wtr, country)

            # Ak sú hráči nájdení a webhook je zadaný, pošli správu
            if players and webhook_url:
                send_to_discord(players, webhook_url)

        except Exception as e:
            error = str(e)

    return render_template("index.html", players=players, error=error)

def get_unclanned_players(min_battles, min_wtr, country):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    player_data = response.json().get("data", [])
    matched_players = []

    for player in player_data:
        account_id = player.get("account_id")
        nickname = player.get("nickname")

        # Info o účte
        info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=statistics"
        info_res = requests.get(info_url)
        if info_res.status_code != 200:
            continue

        info = info_res.json().get("data", {}).get(str(account_id), {})
        if not info or info.get("clan_id") is not None:
            continue

        battles = info.get("statistics", {}).get("all", {}).get("battles", 0)
        wtr = info.get("global_rating", 0)
        country_code = info.get("client_language", "").upper()

        if battles >= min_battles and wtr >= min_wtr:
            if not country or country_code == country:
                matched_players.append({
                    "nickname": nickname,
                    "battles": battles,
                    "wtr": wtr,
                    "country": country_code
                })

    return matched_players

def send_to_discord(players, webhook_url):
    for p in players:
        content = (
            f"**Nájdený hráč bez klanu:**\n"
            f"Prezývka: {p['nickname']}\n"
            f"Bitky: {p['battles']}\n"
            f"WTR: {p['wtr']}\n"
            f"Krajina: {p['country']}"
        )
        payload = {"content": content}
        requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
