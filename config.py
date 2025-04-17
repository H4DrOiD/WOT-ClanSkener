import os

class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'tajny_kluc_pre_wot_skener'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
