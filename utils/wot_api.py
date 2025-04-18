import requests
from config import WARGAMING_API_KEY

def search_players(min_wtr, min_battles, country_code):
    url = f"https://api.worldoftanks.eu/wot/account/list/?application_id={WARGAMING_API_KEY}&limit=100"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    players = []

    for player in data.get("data", []):
        account_id = player.get("account_id")
        nickname = player.get("nickname")

        if account_id:
            player_info = get_account_info(account_id)
            if not player_info:
                continue

            stats = player_info.get("statistics", {}).get("all", {})
            battles = stats.get("battles", 0)
            wtr = player_info.get("global_rating", 0)
            clan_id = player_info.get("clan_id")
            country = player_info.get("client_language", "")

            if (clan_id is None and
                battles >= min_battles and
                wtr >= min_wtr and
                (country_code == "ALL" or country.lower() == country_code.lower())):

                players.append({
                    "nickname": nickname,
                    "account_id": account_id,
                    "battles": battles,
                    "wtr": wtr,
                    "country": country
                })

    return players


def get_account_info(account_id):
    url = f"https://api.worldoftanks.eu/wot/account/info/?application_id={WARGAMING_API_KEY}&account_id={account_id}&extra=clan"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("data", {}).get(str(account_id), {})
