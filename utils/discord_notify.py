import requests

def send_discord_notification(webhook_url, player_data):
    """
    Odosiela notifikáciu o novom hráčovi na Discord webhook.
    :param webhook_url: URL webhooku zadaná veliteľom.
    :param player_data: Slovník s údajmi o hráčovi.
    """
    if not webhook_url:
        return

    nickname = player_data.get("nickname", "Neznámy hráč")
    battles = player_data.get("statistics", {}).get("battles", "N/A")
    rating = player_data.get("global_rating", "N/A")

    message = {
        "content": f"🎯 **Nový hráč bez klanu!**\n"
                   f"**Nick:** {nickname}\n"
                   f"**Počet hier:** {battles}\n"
                   f"**WTR:** {rating}\n"
                   f"<https://eu.wotlife.net/player/{nickname}/>"
    }

    try:
        requests.post(webhook_url, json=message)
    except Exception as e:
        print(f"Chyba pri odosielaní na Discord: {e}")
