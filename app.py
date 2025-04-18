import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "TVOJ_KLUC")
REGIONS = {"eu": "https://api.worldoftanks.eu"}

@app.route("/", methods=["GET", "POST"])
def index():
    players = []

    if request.method == "POST":
        wtr = int(request.form.get("wtr") or 0)
        battles = int(request.form.get("battles") or 0)
        country = request.form.get("country")
        webhook_url = request.form.get("webhook")

        if not webhook_url:
            return render_template("index.html", players=[], error="Musíš zadať Discord webhook URL.")

        # API call
        players = get_unclanned_players(wtr, battles, country)

        if players:
            send_to_discord(players, webhook_url)

    return render_template("index.html", players=players)

def get_unclanned_players(min_wtr, min_battles, country_code):
    # Tu by si implementoval reálnu logiku volania Wargaming API
    # My použijeme simuláciu dát:
    mock_data = [
        {"nickname": "Player1", "battles": 15000, "wtr": 5800, "country": "SK"},
        {"nickname": "Player2", "battles": 5000, "wtr": 4200, "country": "CZ"},
        {"nickname": "Player3", "battles": 3000, "wtr": 3700, "country": "PL"},
    ]

    return [
        player for player in mock_data
        if player["wtr"] >= min_wtr and player["battles"] >= min_battles and player["country"] == country_code
    ]

def send_to_discord(players, webhook_url):
    for player in players:
        message = (
            f"🕹️ **Hráč bez klanu**\n"
            f"Prezývka: {player['nickname']}\n"
            f"Bitky: {player['battles']}\n"
            f"WTR: {player['wtr']}\n"
            f"Krajina: {player['country']}"
        )
        payload = {"content": message}
        try:
            requests.post(webhook_url, json=payload)
        except Exception as e:
            print(f"Chyba pri odosielaní na Discord: {e}")

if __name__ == "__main__":
    app.run(debug=True)
