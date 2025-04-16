import os
import requests

API_ID = os.getenv("WOT_API_ID", "demo")

def search_players_by_nickname(nickname):
    url = "https://api.worldoftanks.eu/wot/account/list/"
    params = {
        "application_id": API_ID,
        "search": nickname,
        "limit": 10
    }
    response = requests.get(url, params=params)
    return response.json()

def get_account_info(account_id):
    url = "https://api.worldoftanks.eu/wot/account/info/"
    params = {
        "application_id": API_ID,
        "account_id": account_id,
        "extra": "statistics"
    }
    response = requests.get(url, params=params)
    return response.json()

Do app.py (v route /, POST časť) 
Kopírovať
Upraviť
from utils.wot_api import search_players_by_nickname, get_account_info

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        nickname = "PantherXx" 
        results = search_players_by_nickname(nickname)
        players = []

        if results.get("status") == "ok":
            for player in results["data"]:
                players.append(player["nickname"])

        return render_template('dashboard.html', players=players, country=country)

    return render_template('index.html')
