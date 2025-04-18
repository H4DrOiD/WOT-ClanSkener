import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

@app.route("/", methods=["GET", "POST"])
def index():
    hraci = []

    if request.method == "POST":
        try:
            min_battles = int(request.form.get("min_battles", 0))
            min_wtr = int(request.form.get("min_wtr", 0))
            krajina = request.form.get("country")
            webhook = request.form.get("webhook")

            hraci = ziskaj_hracov_bez_klanu(min_battles, min_wtr, krajina)

            if hraci and webhook:
                posli_na_discord(hraci, webhook)

        except Exception as e:
            print(f"Chyba: {e}")

    return render_template("index.html", players=hraci)


def ziskaj_hracov_bez_klanu(min_battles, min_wtr, krajina):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100"

    odpoved = requests.get(url)
    if odpoved.status_code != 200:
        return []

    data = odpoved.json().get("data", [])
    vysledok = []

    for hrac in data:
        account_id = hrac["account_id"]
        nickname = hrac["nickname"]

        detail_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=statistics"
        detail_odpoved = requests.get(detail_url)
        detail_data = detail_odpoved.json().get("data", {}).get(str(account_id), {})

        if not detail_data or detail_data.get("clan_id"):
            continue

        bitky = detail_data.get("statistics", {}).get("all", {}).get("battles", 0)
        wtr = detail_data.get("global_rating", 0)
        last_battle = detail_data.get("last_battle_time", "neznáme")
        account_level = detail_data.get("account_level", "neznáme")
        player_country = detail_data.get("client_language", "").upper()

        if bitky >= min_battles and wtr >= min_wtr:
            if krajina == "any" or player_country == krajina:
                vysledok.append({
                    "account_id": account_id,
                    "nickname": nickname,
                    "battles": bitky,
                    "wtr": wtr,
                    "last_battle": last_battle,
                    "account_level": account_level
                })

    return vysledok


def posli_na_discord(hraci, webhook):
    for hrac in hraci:
        message = (
            f"**🎯 Hráč bez klanu:**\n"
            f"**Prezývka:** {hrac['nickname']}\n"
            f"**Bitky:** {hrac['battles']}\n"
            f"**WTR:** {hrac['wtr']}\n"
            f"**Posledná bitka:** {hrac['last_battle']}\n"
            f"**Úroveň účtu:** {hrac['account_level']}"
        )
        payload = {"content": message}
        response = requests.post(webhook, json=payload)

        if response.status_code != 204:
            print(f"⚠️ Chyba pri posielaní na Discord: {response.text}")


if __name__ == "__main__":
    app.run(debug=True)
