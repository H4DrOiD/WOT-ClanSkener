from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Commander(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True, nullable=False)
    clan_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    discord_webhook = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f"<Commander {self.nickname}>"
