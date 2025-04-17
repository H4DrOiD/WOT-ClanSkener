from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Commander(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), unique=True, nullable=False)
    clan_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    webhook_url = db.Column(db.String(300), nullable=True)

