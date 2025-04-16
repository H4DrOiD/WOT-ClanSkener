from flask import Flask, render_template, request
import os
from utils.wot_api import (
    search_players_by_nickname,
    get_account_info,
    get_clan_info,
    get_tank_stats
)
from utils.wn8 import calculate_wn8, load_expected_values

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        wn8_input = request.form.get('wn8')
        battles_input = request.form.get('battles')
        email = request.form.get('email')

        # testovacie meno, neskôr nahradíme generovaním/zoznamom
        test_nickname = "PantherXx"
        api_result = search_players_by_nickname(test_nickname)

        expected_values = load_expected_values()
        players = []

        if api_result.get("status") == "ok":
            for player in api_result["data"]:
                nickname = player["nickname"]
                account_id = player["account_id"]

                # Overenie klanu
                clan_data = get_clan_info(account_id)
                is_clanless = False

                if clan_data.get("status") == "ok":
                    player_data = clan_data["data"].get(str(account_id))
                    if player_data is None or player_data.get("clan") is None:
                        is_clanless = True

                # Získanie tankových štatistík + výpočet WN8
                tank_stats_result = get_tank_stats(account_id)
                wn8 = 0
                battle_count = 0

                if tank_stats_result.get("status") == "ok":
                    tank_data = tank_stats_result["data"].get(str(account_id), [])
                    wn8 = calculate_wn8(tank_data, expected_values)
                    battle_count = sum(t["statistics"]["battles"] for t in tank_data)

                # Overenie podmienok formulára
                min_wn8 = int(wn8) >= int(wn8_input) if wn8_input else True
                min_battles = battle_count >= int(battles_input) if battles_input else True

                if is_clanless and min_wn8 and min_battles:
                    players.append(f"{nickname} | WN8: {wn8} | Bitky: {battle_count}")

        return render_template('dashboard.html', players=players, country=country)

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', players=[], country=None)

@app.route('/privacy')
def privacy():
    return render_template('privacy_policy.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
