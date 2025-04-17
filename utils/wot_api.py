import requests
import os

WG_API_KEY = os.getenv("WARGAMING_API_KEY")
WG_API_BASE_URL = "https://api.worldoftanks.eu/wot"

def search_players(limit=100, min_battles=1000, min_rating=3000, countries=["sk", "cz", "hu", "pl"]):
    all_results = []
    for country in countries:
        players = get_random_players_by_country(country, limit)
        for player in players:
            if not player.get("clan_id") and player.get("statistics", {}).get("battles", 0) >= min_battles:
                rating = player.get("global_rating", 0)
                if rating >= min_rating:
                    all_results.append(player)
    return all_results

def get_random_players_by_country(country, limit=100):
    url = f"{WG_API_BASE_URL}/account/list/"
    params = {
        "application_id": WG_API_KEY,
        "language": "en",
        "search": "",  # necháme prázdne pre random výsledky
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return []

    accounts = data.get("data", [])
    result = []

    for acc in accounts:
        account_id = acc.get("account_id")
        details = get_account_info(account_id)
        if details:
            result.append(details)

    return result

def get_account_info(account_id):
    url = f"{WG_API_BASE_URL}/account/info/"
    params = {
        "application_id": WG_API_KEY,
        "account_id": account_id,
        "extra": "statistics.globalmap"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "ok":
        return None

    return data["data"].get(str(account_id))
