import os

# Flask aplikácia
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "tajny_kluc_pre_flask")

# Wargaming API kľúč
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "vloz_sem_svoj_kod")

# Discord Webhook – použije sa, ak užívateľ neuloží vlastný
DEFAULT_DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

# Povolené krajiny pre filter
ALLOWED_COUNTRIES = ["SK", "CZ", "HU", "PL"]
