from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Commander
from utils.wot_api import get_players_without_clan, send_discord_notification
from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    players = []
    if request.method == 'POST':
        battles = int(request.form.get('battles', 0))
        rating = int(request.form.get('rating', 0))
        country = request.form.get('country')

        players = get_players_without_clan(battles, rating, country)

        # Posielame do všetkých webhookov zaregistrovaných veliteľov
        for commander in Commander.query.all():
            if commander.webhook:
                send_discord_notification(commander.webhook, players)

    return render_template('index.html', players=players)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form['nickname']
        clan_name = request.form['clan_name']
        password = generate_password_hash(request.form['password'])
        webhook = request.form['webhook']

        existing_user = Commander.query.filter_by(nickname=nickname).first()
        if existing_user:
            flash("Tento používateľ už existuje.")
            return redirect(url_for('routes.register'))

        user = Commander(nickname=nickname, clan_name=clan_name, password=password, webhook=webhook)
        db.session.add(user)
        db.session.commit()
        flash("Registrácia úspešná. Môžeš sa prihlásiť.")
        return redirect(url_for('routes.login'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        user = Commander.query.filter_by(nickname=nickname).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.profile'))
        flash("Nesprávne prihlasovacie údaje.")

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        webhook = request.form['webhook']
        current_user.webhook = webhook
        db.session.commit()
        flash("Webhook bol aktualizovaný.")
        return redirect(url_for('routes.profile'))

    return render_template('profile.html', user=current_user)
