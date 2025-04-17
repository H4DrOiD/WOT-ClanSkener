from flask import Flask, render_template, request, redirect, url_for
import requests
from utils.wot_api import get_player_stats

app = Flask(__name__)

# Predpokladám, že tu si uložíš svoj discord webhook
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    nickname = request.form['nickname']
    stats, wn8 = get_player_stats(nickname)
    
    if stats:
        # Posielame údaje do Discordu
        send_to_discord(stats, wn8)
        return render_template('result.html', stats=stats, wn8=wn8, nickname=nickname)
    else:
        return render_template('index.html', message="Player not found!")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Tu implementuješ registráciu veliteľa
        username = request.form['username']
        password = request.form['password']
        clan_name = request.form['clan_name']
        
        # Uložíš informácie do databázy alebo do konfigurácie
        # Zatiaľ len placeholder
        return redirect(url_for('index'))
    return render_template('register.html')

def send_to_discord(stats, wn8):
    data = {
        "content": f"New Player Stats:\n\n{stats}\nWN8: {wn8}",
        "username": "WOT-ClanSkener Bot",
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

if __name__ == '__main__':
    app.run(debug=True)
