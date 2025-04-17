from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Commander(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    clan_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    webhook = db.Column(db.String(300), nullable=True)

    def get_id(self):
        return str(self.id)
