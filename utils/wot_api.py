import requests
import json
import os

WARGAMING_API_KEY = os.getenv('WARGAMING_API_KEY')
BASE_URL = "https://api.worldoftanks.eu/wot"

def get_player_stats(nickname):
    """
    Získanie štatistík hráča z API World of Tanks.
    """
    url = f"{BASE_URL}/account/info/"
    params = {
        'application_id': WARGAMING_API_KEY,
        'search': nickname
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        player_data = data['data']
        if nickname in player_data:
            stats = player_data[nickname]
            wn8 = calculate_wn8(stats)
            return stats, wn8
    return None, None

def calculate_wn8(stats):
    """
    Vypočíta hodnotu WN8 podľa hráčskych štatistík.
    """
    # Tu môžeš pridať algoritmus na výpočet WN8 (hodnota WN8 sa počíta na základe rôznych faktorov ako presnosť, výhry, atď.)
    wn8 = stats['battle_avg']['damage'] * 100  # Toto je iba príklad
    return wn8
