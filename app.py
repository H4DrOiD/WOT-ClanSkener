import os
from flask import Flask, render_template, request
from utils.wot_api import search_players_by_nickname, get_account_info

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    country_filter = request.form.get("country")
    
    if request.method == "POST":
        nickname = request.form.get("nickname")
        if nickname:
            search_results = search_players_by_nickname(nickname)
            if search_results and search_results.get("status") == "ok":
                for result in search_results["data"]:
                    account_id = result["account_id"]
                    info = get_account_info(account_id)
                    if info and info.get("status") == "ok":
                        player_data = info["data"].get(str(account_id), {})
                        if player_data and not player_data.get("clan_id"):
                            if not country_filter or country_filter == "any" or player_data.get("client_language") == country_filter:
                                players.append({
                                    "nickname": player_data.get("nickname"),
                                    "battles": player_data.get("statistics", {}).get("all", {}).get("battles"),
                                    "wn8": "N/A",  # môže byť doplnené neskôr
                                    "country": player_data.get("client_language", "N/A")
                                })

    return render_template("index.html", players=players)

if __name__ == "__main__":
    app.run(debug=True)
