import os
from flask import Flask, render_template, request, redirect, url_for, session
from utils.db import init_db, get_users_without_clan, register_commander, verify_commander
from utils.discord import send_discord_notification

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "tajneheslo")
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        battles = int(request.form.get("battles", 0))
        wtr = int(request.form.get("wtr", 0))
        country = request.form.get("country", "")

        players = get_users_without_clan(battles, wtr, country)

        # Ak je veliteľ prihlásený a má webhook
        if "username" in session:
            username = session["username"]
            send_discord_notification(players, username)

        return render_template("index.html", players=players, country=country, battles=battles, wtr=wtr)

    return render_template("index.html", players=[])

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nickname = request.form["nickname"]
        clan_name = request.form["clan_name"]
        password = request.form["password"]
        webhook = request.form["webhook"]
        register_commander(nickname, clan_name, password, webhook)
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]
        if verify_commander(nickname, password):
            session["username"] = nickname
            return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
