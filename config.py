import os

# Wargaming API kľúč (získaný z developers.wargaming.net)
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

# Discord webhook kam sa odošlú notifikácie
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU")
