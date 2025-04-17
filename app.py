from flask import Flask, render_template, request, redirect, url_for, jsonify
from utils.wot_api import get_player_stats
import os
import json
import requests

app = Flask(__name__)

# Počiatočné nastavenie pre webhook
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nickname = request.form.get("nickname")
        stats, wn8 = get_player_stats(nickname)
        
        if stats:
            return render_template("results.html", stats=stats, wn8=wn8)
        else:
            return render_template("error.html", message="Player not found or invalid.")

    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if 'event' in data:
        send_to_discord(data)
    return jsonify({"status": "success"}), 200

def send_to_discord(data):
    """
    Funkcia na odoslanie informácií na Discord cez webhook.
    """
    message = {
        "content": f"New player found: {data['player_name']}, WN8: {data['wn8']}"
    }
    
    response = requests.post(DISCORD_WEBHOOK, json=message)
    if response.status_code != 204:
        print(f"Failed to send data to Discord: {response.status_code}")

if __name__ == "__main__":
    app.run(debug=True)
