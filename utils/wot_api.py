import requests
import json
import os

# API kľúč Wargaming
WG_API_KEY = os.getenv('WG_API_KEY')  # Uisti sa, že tento kľúč je v environment variables

# Funkcia na získanie štatistík hráča
def get_player_stats(nickname):
    url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WG_API_KEY}&search={nickname}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok' and len(data['data']) > 0:
        player_data = data['data'].popitem()[1]  # Zoberieme prvého hráča zo zoznamu
        player_name = player_data['nickname']
        battles = player_data['statistics']['battles']
        wn8 = player_data['statistics']['wn8']
        
        stats = {
            "nickname": player_name,
            "battles": battles,
            "wn8": wn8,
        }
        
        return stats, wn8
    else:
        return None, None
