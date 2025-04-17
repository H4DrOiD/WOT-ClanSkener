import requests
import os

# Definuj svoj API kľúč
API_KEY = os.getenv("WARGAMING_API_KEY")
BASE_URL = "https://api.worldoftanks.eu/wot/"

def get_player_stats(nickname):
    """
    Získaj štatistiky hráča podľa jeho prezývky.
    """
    url = f"{BASE_URL}account/info/?application_id={API_KEY}&search={nickname}"
    response = requests.get(url)
    data = response.json()
    
    if data.get('status') == 'ok':
        player_data = data['data']
        if nickname in player_data:
            player = player_data[nickname]
            wn8 = calculate_wn8(player)
            stats = {
                'nickname': player['nickname'],
                'battles': player['statistics']['battles'],
                'wins': player['statistics']['wins'],
                'wn8': wn8
            }
            return stats, wn8
    return None, None

def calculate_wn8(player_data):
    """
    Vypočíta hodnotu WN8 na základe štatistík hráča.
    """
    battles = player_data['statistics']['battles']
    damage_dealt = player_data['statistics']['damage_dealt']
    frags = player_data['statistics']['frags']
    
    wn8 = (damage_dealt * 0.5) + (frags * 0.3)  # Jednoduchý výpočet WN8
    return round(wn8, 2)
