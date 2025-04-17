import sqlite3

DB_FILE = 'database.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            clan_name TEXT NOT NULL,
            password TEXT NOT NULL,
            webhook_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(nickname, clan_name, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (nickname, clan_name, password) VALUES (?, ?, ?)',
                   (nickname, clan_name, password))
    conn.commit()
    conn.close()

def authenticate_user(nickname, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE nickname = ? AND password = ?', (nickname, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_nickname(nickname):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE nickname = ?', (nickname,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_webhook(nickname, webhook_url):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET webhook_url = ? WHERE nickname = ?', (webhook_url, nickname))
    conn.commit()
    conn.close()
