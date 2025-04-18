import requests
import os

API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

def search_players(wtr_min, battles_min, country_filter):
    search_url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={API_KEY}&limit=100&status=available"
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"Chyba pri volaní API: {response.text}")
        return []

    players = []
    for player in response.json().get("data", []):
        account_id = player.get("account_id")
        nickname = player.get("nickname")

        # Získaj detailné štatistiky
        details_url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={API_KEY}&account_id={account_id}&extra=statistics"
        details_res = requests.get(details_url)
        info = details_res.json()["data"].get(str(account_id), {})

        battles = info.get("statistics", {}).get("all", {}).get("battles", 0)
        wtr = info.get("global_rating", 0)
        clan_id = info.get("clan_id", None)
        country = info.get("private", {}).get("country", "unknown")

        if (
            clan_id is None and
            battles >= battles_min and
            wtr >= wtr_min and
            (country_filter == "ALL" or country.lower() == country_filter.lower())
        ):
            players.append({
                "nickname": nickname,
                "battles": battles,
                "wtr": wtr,
                "country": country.upper()
            })

    return players
