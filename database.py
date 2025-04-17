import sqlite3

DATABASE_FILE = "clanskener.db"

def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Tabuľka pre veliteľov
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commanders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            clan_name TEXT,
            password TEXT NOT NULL,
            discord_webhook TEXT
        )
    """)
    
    # Tabuľka pre uloženie posledných notifikovaných hráčov (voliteľné)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notified_players (
            account_id INTEGER PRIMARY KEY,
            notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn
