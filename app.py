import os
from flask import Flask, render_template, request
from utils.wot_api import search_players
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    if request.method == "POST":
        try:
            min_battles = int(request.form.get("min_battles", 0))
            min_wtr = int(request.form.get("min_wtr", 0))
            country = request.form.get("country", "ALL")
            webhook_url = request.form.get("webhook_url")

            players = search_players(min_wtr, min_battles, country)

            if webhook_url and players:
                send_to_discord(players, webhook_url)

        except Exception as e:
            print(f"Chyba: {e}")

    return render_template("index.html", players=players)

def send_to_discord(players, webhook_url):
    content = "**Hráči bez klanu podľa kritérií:**\n"
    for player in players:
        content += (
            f"🔸 **{player['nickname']}** | Bitky: {player['battles']} | WTR: {player['wtr']} | Krajina: {player['country']}\n"
        )

    payload = {"content": content}
    requests.post(webhook_url, json=payload)

if __name__ == "__main__":
    app.run(debug=True)
