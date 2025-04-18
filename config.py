import os

# Wargaming API kľúč
WARGAMING_API_KEY = os.getenv("WARGAMING_API_KEY", "vloz_sem_svoj_kluc")

# Discord Webhook (dočasne testovací)
DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL",
    "https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU"
)

# Počet hráčov, ktorých chceme získať z API (limit)
SEARCH_LIMIT = 100

# Dostupné krajiny pre výber
SUPPORTED_COUNTRIES = ["SK", "CZ", "PL", "HU", "UK"]
