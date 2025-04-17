from flask import Flask, render_template, request, redirect, url_for, session
from utils.wot_api import get_player_stats
import os
import requests
import json

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    nickname = request.form['nickname']
    country = request.form['country']
    battles = int(request.form['battles'])

    stats, wn8 = get_player_stats(nickname)
    
    if stats and stats['battles'] >= battles:
        return render_template('results.html', stats=stats, wn8=wn8)
    else:
        return render_template('index.html', error="No matching player found")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        clan_name = request.form['clan_name']
        password = request.form['password']
        
        # Tu by si mal uložiť registračné údaje do databázy
        # Napríklad uložiť do databázy SQLite alebo MySQL
        
        # Presmerovanie po úspešnej registrácii
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Tu by sa malo skontrolovať užívateľské meno a heslo
        # Napríklad skontrolovať v databáze
        
        # Ak sú údaje správne, prihlásime užívateľa
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Ak nie je prihlásený, presmerujeme ho na prihlásenie
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

if __name__ == '__main__':
    app.run(debug=True)
