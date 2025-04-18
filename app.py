import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    if request.method == "POST":
        wtr = request.form.get("wtr")
        battles = request.form.get("battles")
        country = request.form.get("country")
        webhook_url = request.form.get("webhook")

        if not webhook_url:
            return render_template("index.html", error="Webhook URL je povinné.")

        # Tu sa neskôr pridá volanie API Wargaming a filtrovanie hráčov bez klanu
        # Teraz pošleme len testovaciu správu do Discord webhooku

        test_message = f"Vyhľadávanie spustené:\nWTR: {wtr}, Hry: {battles}, Krajina: {country}"
        requests.post(webhook_url, json={"content": test_message})

        # Testovací hráči (simulácia)
        players = [
            {"nickname": "PlayerOne", "wtr": 5300, "battles": 15000, "country": "SK"},
            {"nickname": "PlayerTwo", "wtr": 4800, "battles": 12000, "country": "CZ"},
        ]

    return render_template("index.html", players=players)

if __name__ == "__main__":
    app.run(debug=True)
