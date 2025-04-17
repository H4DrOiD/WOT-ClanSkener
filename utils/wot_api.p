import requests
import os

WG_API_KEY = os.getenv("WARGAMING_API_KEY")

def get_players_without_clan(min_battles, min_rating, country):
    url = "https://api.worldoftanks.eu/wgn/account/list/"
    params = {
        "application_id": WG_API_KEY,
        "search": "",  # V skutočnosti by sme potrebovali list account_id, toto je len simulácia
        "limit": 100
    }

    response = requests.get(url, params=params)
    data = response.json()

    filtered_players = []

    if data.get("status") != "ok":
        return []

    for player in data.get("data", []):
        account_id = player.get("account_id")
        info = get_account_info(account_id)

        if not info or info.get("clan_id"):
            continue

        stats = info.get("statistics", {}).get("all", {})
        battles = stats.get("battles", 0)
        rating = info.get("global_rating", 0)

        if battles >= min_battles and rating >= min_rating:
            if country and info.get("client_language") not in [country.lower(), ""]:
                continue

            filtered_players.append({
                "nickname": player.get("nickname"),
                "battles": battles,
                "rating": rating
            })

    return filtered_players

def get_account_info(account_id):
    url = f"https://api.worldoftanks.eu/wot/account/info/"
    params = {
        "application_id": WG_API_KEY,
        "account_id": account_id,
        "fields": "statistics.all.battles,global_rating,clan_id,client_language"
    }

    response = requests.get(url, params=params)
    data = response.json()
    if data.get("status") == "ok":
        return data.get("data", {}).get(str(account_id))
    return None

def send_discord_notification(webhook_url, players):
    if not players:
        return

    message = "**🔍 Noví hráči bez klanu spĺňajúci kritériá:**\n"
    for player in players:
        message += f"- {player['nickname']} | Bitky: {player['battles']} | WTR: {player['rating']}\n"

    payload = {
        "content": message
    }

    try:
        requests.post(webhook_url, json=payload)
    except Exception as e:
        print(f"⚠️ Chyba pri odosielaní na Discord: {e}")
