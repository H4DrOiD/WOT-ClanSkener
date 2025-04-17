import os

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "tajny_kluc_na_vyvoj")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
