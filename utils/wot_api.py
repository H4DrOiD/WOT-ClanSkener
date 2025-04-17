import os
import requests

WG_API_KEY = os.getenv("WARGAMING_API_KEY")

BASE_URL = "https://api.worldoftanks.eu/wot"


def get_players_without_clan(min_battles=0, min_wtr=0, nations=None, limit=100):
    search_url = f"{BASE_URL}/account/list/"
    params = {
        "application_id": WG_API_KEY,
        "limit": limit,
        "fields": "nickname,account_id",
        "search": "",  # empty string returns general users
    }
    response = requests.get(search_url, params=params)
    result = []

    if response.status_code == 200 and response.json().get("status") == "ok":
        data = response.json().get("data", [])
        for player in data:
            account_id = player.get("account_id")
            info = get_account_info(account_id)
            if info and info.get("clan_id") is None:
                battles = info.get("statistics", {}).get("all", {}).get("battles", 0)
                wtr = info.get("global_rating", 0)
                country = info.get("country", "").upper()

                if (
                    battles >= min_battles
                    and wtr >= min_wtr
                    and (not nations or country in nations)
                ):
                    result.append({
                        "nickname": info.get("nickname"),
                        "battles": battles,
                        "wtr": wtr,
                        "country": country,
                    })

    return result


def get_account_info(account_id):
    info_url = f"{BASE_URL}/account/info/"
    params = {
        "application_id": WG_API_KEY,
        "account_id": account_id,
        "fields": "nickname,clan_id,statistics.global_rating,statistics.all.battles"
    }
    response = requests.get(info_url, params=params)

    if response.status_code == 200 and response.json().get("status") == "ok":
        data = response.json().get("data", {})
        return data.get(str(account_id))
    return None
