import os
from flask import Flask, render_template, request
from utils.wot_api import (
    search_players_by_nickname,
    get_account_info,
    get_tank_stats,
    calculate_wn8,
)

app = Flask(__name__)
app.secret_key = os.getenv("29b6e96e5fa1462cbebfb386fb565a0d", "981118")

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    error_message = None
    selected_country = None

    if request.method == "POST":
        selected_country = request.form.get("country")
        nicknames_input = request.form.get("nicknames")

        if not nicknames_input:
            error_message = "Zadaj aspoň jeden nick."
        else:
            nicknames = [nick.strip() for nick in nicknames_input.splitlines()]
            try:
                for nick in nicknames:
                    account_id = search_players_by_nickname(nick)
                    if not account_id:
                        continue

                    account_info = get_account_info(account_id)
                    tank_stats = get_tank_stats(account_id)
                    wn8 = calculate_wn8(tank_stats)

                    players.append({
                        "nickname": nick,
                        "account_id": account_id,
                        "battles": account_info.get("statistics", {}).get("all", {}).get("battles", 0),
                        "wn8": round(wn8, 2) if wn8 else "N/A"
                    })
            except Exception as e:
                print(f"Chyba: {e}")
                error_message = "Vyskytla sa chyba pri spracovaní hráčov."

    return render_template("index.html", players=players, country=selected_country, error=error_message)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request
from utils.wot_api import search_players_by_nickname  # Uisti sa, že táto funkcia existuje a vracia zoznam hráčov

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    players = []
    country = ""
    if request.method == "POST":
        nickname = request.form.get("nickname")
        country = request.form.get("country")

        # Testovacie výpisy
        print(f"Zadaný nickname: {nickname}")
        print(f"Zadaná krajina: {country}")

        try:
            if nickname:
                players = search_players_by_nickname(nickname, country)
            else:
                # Dočasný testovací fallback pre zobrazenie výsledkov
                players = [
                    {"nickname": "TestPlayer1", "wn8": 2150, "battles": 1500},
                    {"nickname": "TestPlayer2", "wn8": 1790, "battles": 980}
                ]
        except Exception as e:
            print(f"Chyba pri vyhľadávaní hráčov: {e}")
    
    return render_template("index.html", players=players, country=country)
