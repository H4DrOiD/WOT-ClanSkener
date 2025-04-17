import os

# Flask aplikácia
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "981118")

# Wargaming API kľúč
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "29b6e96e5fa1462cbebfb386fb565a0d")

# Discord Webhook – použije sa, ak užívateľ neuloží vlastný
DEFAULT_DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU")

# Povolené krajiny pre filter
ALLOWED_COUNTRIES = ["SK", "CZ", "HU", "PL"]
