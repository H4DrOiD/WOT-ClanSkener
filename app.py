import os
import requests
from flask import Flask, render_template, request
from datetime import datetime
from utils.wot_api import search_players_by_nickname, get_account_info

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    error = None

    if request.method == "POST":
        try:
            min_battles = int(request.form["min_battles"])
            min_winrate = float(request.form["min_winrate"])

            # Získanie hráčov bez klanu z externého API (napr. wot api alebo uloženého datasetu)
            search_url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={os.getenv('WARGAMING_API_KEY')}&search=&limit=100"
            response = requests.get(search_url).json()

            if response["status"] == "ok":
                for item in response["data"]:
                    account_id = item["account_id"]

                    info_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={os.getenv('WARGAMING_API_KEY')}&account_id={account_id}"
                    info_response = requests.get(info_url).json()

                    if info_response["status"] == "ok":
                        data = info_response["data"][str(account_id)]
                        if not data["clan_id"]:  # hráč nie je v klane
                            battles = data["statistics"]["all"]["battles"]
                            wins = data["statistics"]["all"]["wins"]
                            winrate = round((wins / battles) * 100, 2) if battles > 0 else 0
                            last_battle_ts = data["last_battle_time"]
                            last_battle_time = datetime.utcfromtimestamp(last_battle_ts).strftime('%Y-%m-%d') if last_battle_ts else "N/A"

                            if battles >= min_battles and winrate >= min_winrate:
                                players.append({
                                    "account_id": account_id,
                                    "nickname": data["nickname"],
                                    "battles": battles,
                                    "winrate": winrate,
                                    "last_battle_time": last_battle_time
                                })
            else:
                error = "Nepodarilo sa načítať údaje z API."

        except Exception as e:
            error = f"Chyba: {str(e)}"

    return render_template("index.html", players=players, error=error)

if __name__ == "__main__":
    app.run(debug=True)
