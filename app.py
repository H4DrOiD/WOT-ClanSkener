import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Wargaming API Key (dočasne vložte kľúč z Wargaming API)
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

# Discord webhook URL (pridajte svoju URL, alebo použite testovaciu)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    if request.method == "POST":
        nickname = request.form.get("nickname")
        country = request.form.get("country")
        min_battles = int(request.form.get("min_battles"))
        min_wn8 = int(request.form.get("min_wn8"))
        
        # Volanie funkcie na získanie hráčov
        players = get_players_without_clan(nickname, country, min_battles, min_wn8)
        
        if players:
            # Po nájdení hráčov odošleme informácie na Discord cez webhook
            send_discord_notification(players)

    return render_template("index.html", players=players)

def get_players_without_clan(nickname, country, min_battles, min_wn8):
    # Vytvorenie URL pre Wargaming API
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&search={nickname}&limit=100"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        players = []
        
        for player in data.get('data', []):
            # Získanie potrebných údajov o hráčovi
            player_battles = player.get("statistics", {}).get("all", {}).get("battles", 0)
            player_wn8 = player.get("statistics", {}).get("all", {}).get("wn8", 0)
            player_country = player.get("country", "")
            clan = player.get("clan", None)

            # Filter podľa zadaných kritérií
            if player_battles >= min_battles and player_wn8 >= min_wn8 and clan is None and player_country == country:
                players.append({
                    "nickname": player["nickname"],
                    "battles": player_battles,
                    "wn8": player_wn8,
                    "country": player_country
                })
        return players
    else:
        return []

def send_discord_notification(players):
    # Vytvorenie JSON payloadu pre Discord webhook
    for player in players:
        message = f"**Nový hráč bez klanu:**\n"
        message += f"Prezývka: {player['nickname']}\n"
        message += f"Počet bitiek: {player['battles']}\n"
        message += f"WN8: {player['wn8']}\n"
        message += f"Krajina: {player['country']}"

        payload = {"content": message}
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if response.status_code != 204:
            print(f"Chyba pri posielaní notifikácie na Discord: {response.text}")

if __name__ == "__main__":
    app.run(debug=True)

