import os
import requests

API_ID = os.getenv("WOT_API_ID", "demo")

def search_players_by_nickname(nickname):
    url = "https://api.worldoftanks.eu/wot/account/list/"
    params = {
        "application_id": API_ID,
        "search": nickname,
        "limit": 10
    }
    response = requests.get(url, params=params)
    return response.json()

def get_account_info(account_id):
    url = "https://api.worldoftanks.eu/wot/account/info/"
    params = {
        "application_id": API_ID,
        "account_id": account_id,
        "extra": "statistics"
    }
    response = requests.get(url, params=params)
    return response.json()
