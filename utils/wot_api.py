import requests
import os
import json

WG_API_KEY = os.getenv("29b6e96e5fa1462cbebfb386fb565a0d")

# 🔍 Vyhľadá hráčov podľa prefixu (napr. "a", "b", atď.)
def search_players_by_nickname(prefix, limit=10):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WG_API_KEY}&search={prefix}&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return data.get("data", [])

# ℹ️ Získa základné info o hráčovi (bitky, meno atď.)
def get_account_info(account_id):
    url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WG_API_KEY}&account_id={account_id}"
    response = requests.get(url)
    data = response.json()

    player_data = data.get("data", {}).get(str(account_id), {})
    battles = player_data.get("statistics", {}).get("all", {}).get("battles", 0)
    return {
        "battles": battles
    }

# 📊 Získa štatistiky tankov hráča
def get_tank_stats(account_id):
    url = f"https://api.worldoftanks.eu/wot/tanks/stats/?application_id={WG_API_KEY}&account_id={account_id}"
    response = requests.get(url)
    data = response.json()

    return data.get("data", {}).get(str(account_id), [])

# 🧮 Vypočíta zjednodušený WN8 – len informatívny výpočet
def calculate_wn8(tank_stats):
    total_damage = sum(t.get("damage_dealt", 0) for t in tank_stats)
    total_frags = sum(t.get("frags", 0) for t in tank_stats)
    total_spots = sum(t.get("spotted", 0) for t in tank_stats)
    total_def = sum(t.get("defense_points", 0) for t in tank_stats)
    total_wins = sum(t.get("wins", 0) for t in tank_stats)
    total_battles = sum(t.get("battles", 0) for t in tank_stats)

    if total_battles == 0:
        return 0

    wn8 = (
        (total_damage / total_battles) * 0.4 +
        (total_frags / total_battles) * 0.3 +
        (total_spots / total_battles) * 0.1 +
        (total_def / total_battles) * 0.1 +
        (total_wins / total_battles) * 0.1
    )
    return round(wn8, 2)

# 🧩 Export dostupných funkcií
__all__ = [
    "search_players_by_nickname",
    "get_account_info",
    "get_tank_stats",
    "calculate_wn8"
]
    
