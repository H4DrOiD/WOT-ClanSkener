import os
import requests

WG_API_KEY = os.getenv("29b6e96e5fa1462cbebfb386fb565a0d")
API_URL = "https://api.worldoftanks.eu/wot"

def search_players_by_nickname(nickname):
    url = f"{API_URL}/account/list/"
    params = {
        "application_id": WG_API_KEY,
        "search": nickname,
        "type": "exact"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("Chyba pri vyhľadávaní hráča:", e)
        return None

def get_account_info(account_id):
    url = f"{API_URL}/account/info/"
    params = {
        "application_id": WG_API_KEY,
        "account_id": account_id,
        "extra": "statistics"
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print("Chyba pri získavaní údajov hráča:", e)
        return None
