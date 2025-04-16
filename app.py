from flask import Flask, render_template, request
import os
import json
from utils.wot_api import search_players_by_nickname, get_account_info, get_tank_stats, calculate_wn8

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    debug_info = {"checked": 0, "found": 0, "matched": 0}

    if request.method == "POST":
        wn8_min = int(request.form.get("wn8", 0))
        battles_min = int(request.form.get("battles", 0))
        country = request.form.get("country")
        email = request.form.get("email")

        import string
        search_prefixes = list(string.ascii_lowercase) + [str(i) for i in range(10)] + list("-_.+=@")

        for prefix in search_prefixes:
            players = search_players_by_nickname(prefix)
            debug_info["checked"] += len(players)

            for player in players:
                if player.get("clan_id"):
                    continue  # hráč je v klane

                debug_info["found"] += 1
                account_id = player["account_id"]
                info = get_account_info(account_id)
                stats = get_tank_stats(account_id)
                wn8 = calculate_wn8(stats)

                if info["battles"] >= battles_min and wn8 >= wn8_min:
                    player["wn8"] = wn8
                    player["battles"] = info["battles"]
                    results.append(player)
                    debug_info["matched"] += 1

        results = sorted(results, key=lambda x: x["wn8"], reverse=True)

    return render_template("index.html", results=results, debug=debug_info)

if __name__ == "__main__":
    app.run(debug=True)
