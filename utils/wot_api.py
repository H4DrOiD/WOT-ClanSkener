import os
import requests

WG_API_KEY = os.getenv("WARGAMING_API_KEY")

WG_API_BASE = "https://api.worldoftanks.eu/wot"

def search_players_without_clan(realm="eu", min_battles=1000, min_rating=5000, countries=None):
    """Vyhľadá hráčov bez klanu podľa zadaných kritérií."""

    url = f"{WG_API_BASE}/account/list/"
    params = {
        "application_id": WG_API_KEY,
        "search": "",  # prázdne, aby sme získali všetkých
        "limit": 100,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "ok":
            print("Chyba pri načítaní hráčov:", data.get("error", {}))
            return []

        player_ids = [entry["account_id"] for entry in data["data"]]
        return filter_players(player_ids, min_battles, min_rating, countries)

    except Exception as e:
        print("Chyba pri vyhľadávaní hráčov:", e)
        return []

def filter_players(player_ids, min_battles, min_rating, countries):
    """Filtrovanie hráčov podľa parametrov (bitky, rating, krajina)."""
    url = f"{WG_API_BASE}/account/info/"
    params = {
        "application_id": WG_API_KEY,
        "account_id": ",".join(map(str, player_ids)),
        "fields": "statistics.all.battles,global_rating,nickname,clan_id"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "ok":
            print("Chyba pri filtrovaní hráčov:", data.get("error", {}))
            return []

        filtered = []
        for account_id, player in data["data"].items():
            if not player:
                continue

            nickname = player.get("nickname")
            battles = player.get("statistics", {}).get("all", {}).get("battles", 0)
            rating = player.get("global_rating", 0)
            clan_id = player.get("clan_id", None)

            if clan_id is not None:
                continue  # hráč už má klan

            if battles >= min_battles and rating >= min_rating:
                filtered.append({
                    "nickname": nickname,
                    "battles": battles,
                    "rating": rating,
                    "account_id": account_id
                })

        return filtered

    except Exception as e:
        print("Chyba pri filtrovaní hráčov:", e)
        return []
