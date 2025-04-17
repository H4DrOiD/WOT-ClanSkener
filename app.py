import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Nahradenie s environment variables pre bezpečnosť
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY")

def get_players(nickname, country, min_battles, min_wn8):
    url = f'https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&search={nickname}&language={country}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        players = []
        for player in data.get("data", []):
            if player.get('statistics', {}).get('battles', 0) >= min_battles:
                wn8 = calculate_wn8(player['statistics'])  # Toto si predpokladajte, že máte definovanú funkciu na výpočet WN8
                if wn8 >= min_wn8:
                    players.append({
                        'nickname': player.get('nickname'),
                        'battles': player['statistics'].get('battles'),
                        'wn8': wn8,
                        'country': player['country']
                    })
        return players
    return []

@app.route('/', methods=['GET', 'POST'])
def index():
    players = []
    if request.method == 'POST':
        nickname = request.form.get('nickname', '')
        country = request.form.get('country', 'SK')
        min_battles = int(request.form.get('min_battles', 100))
        min_wn8 = int(request.form.get('min_wn8', 1000))
        
        players = get_players(nickname, country, min_battles, min_wn8)
    
    return render_template('index.html', players=players)

# Funkcia na výpočet WN8 z údajov
def calculate_wn8(stats):
    # Tento výpočet je zjednodušený a mal by byť prispôsobený reálnemu výpočtu WN8
    wn8 = (stats['damage_dealt'] / stats['battles']) * 1000
    return round(wn8)

if __name__ == "__main__":
    app.run(debug=True)
