import os
from flask import Flask, render_template, request
from utils.wot_api import (
    search_players_by_nickname,
    get_account_info,
    get_tank_stats,
    calculate_wn8
)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "tajny_kluc_pre_dev")

@app.route("/", methods=["GET", "POST"])
def index():
    print("➡️ Vstup do index()")  # TEST

    players = []
    country = ""

    if request.method == "POST":
        print("🟢 Prijatý POST request!")  # TEST

        nickname = request.form.get("nickname")
        country = request.form.get("country")

        print(f"🔍 Zadaný nickname: {nickname}")  # TEST
        print(f"🌍 Zadaná krajina: {country}")    # TEST

        # TESTOVACÍ FAKE VÝSTUP – kým API nie je zapojené
        if nickname:
            players = [
                {"nickname": nickname, "wn8": 1580, "battles": 2450}
            ]
            print("✅ Pridávam testovacieho hráča do výstupu.")
        else:
            print("❌ Nickname nebol zadaný.")

    return render_template("index.html", players=players, country=country)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

if __name__ == "__main__":
    app.run(debug=True)
