import os

# Wargaming API key – buď z prostredia, alebo fallback string
WG_API_KEY = os.getenv("29b6e96e5fa1462cbebfb386fb565a0d")

# Flask tajný kľúč
FLASK_SECRET_KEY = os.getenv("981118")

# E-mailové údaje na odosielanie upozornení
EMAIL_ADDRESS = os.getenv("wotclanskener@gmail.com")
EMAIL_PASSWORD = os.getenv("Jeden1Dva2Tri3")

# Discord webhook – môžeš nechať prázdne, ak sa nepoužíva
DISCORD_WEBHOOK = os.getenv("https://discordapp.com/api/webhooks/1361927609256116234/1DKfAyKhdw5aZ69hw2qoJLfNjP_mt0mlXLZTeHLeYrHer6CK3UIPCIDQ74nLm3m2ohhU")

# Jazyk a región pre Wargaming API
API_LANGUAGE = "en"
WOT_REALM = "eu"

# Prípadné ďalšie nastavenia
DEBUG_MODE = True
BASE_WOT_API = "https://api.worldoftanks.eu/wot/"
