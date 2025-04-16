from flask import Flask, render_template, request
import os
from utils.wot_api import search_players_by_nickname, get_account_info

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        wn8 = request.form.get('wn8')
        battles = request.form.get('battles')
        email = request.form.get('email')

        test_nickname = "PantherXx"
        api_result = search_players_by_nickname(test_nickname)

        players = []

        if api_result.get("status") == "ok":
            for player in api_result["data"]:
                nickname = player["nickname"]
                account_id = player["account_id"]
                players.append(f"{nickname} (ID: {account_id})")

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
