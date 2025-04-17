import requests
import json

WARGAMING_API_URL = "https://api.worldoftanks.eu/wot/account/"
WARGAMING_API_KEY = '29b6e96e5fa1462cbebfb386fb565a0d'  # Zadaj svoj Wargaming API kľúč

def search_players_by_nickname(nickname):
    url = f"{WARGAMING_API_URL}list/?application_id={WARGAMING_API_KEY}&search={nickname}"
    response = requests.get(url)
    return response.json()

def get_account_info(account_id):
    url = f"{WARGAMING_API_URL}info/?application_id={WARGAMING_API_KEY}&account_id={account_id}"
    response = requests.get(url)
    return response.json()

def get_tank_stats(account_id):
    url = f"https://api.worldoftanks.eu/wot/account/tanks/?application_id={WARGAMING_API_KEY}&account_id={account_id}"
    response = requests.get(url)
    return response.json()

def calculate_wn8(account_id):
    stats = get_account_info(account_id)
    battles = stats.get("data", {}).get(str(account_id), {}).get("statistics", {}).get("all", {}).get("battles", 0)
    wn8 = 0  # Tu bude tvoja implementácia výpočtu WN8, môžeš využiť externé knižnice alebo vlastný výpočet
    return wn8

def get_player_stats(nickname):
    player_data = search_players_by_nickname(nickname)
    if player_data.get("status") == "ok":
        player_info = player_data["data"]
        if player_info:
            account_id = player_info[0]["account_id"]
            stats = get_account_info(account_id)
            wn8 = calculate_wn8(account_id)
            return stats, wn8
    return None, None
