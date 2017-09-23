from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    game_bit_balance = db.Column(db.Float)
    game_usd_balance = db.Column(db.Float)

#game should be managed by admins
class Gameinfo(db.Model):
    round_id = db.Column(db.Integer, primary_key = True)
    round_time = db.Column(db.DateTime, unique = True)

class Gameplayer(db.Model):
    round_id = db.Column(db.Integer, db.ForeignKey('gameinfo.round_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Usergametransactions(db.Model):
    transaction_id = db.Column(db.Integer, primary_key = True)
    game_round_id = db.Column(db.Integer, db.ForeignKey('gameinfo.round_id'))
    amout = db.Column(db.Float)
    bitcoin_price = db.Column(db.Float)
    transaction_time = db.Column(db.DateTime)
    transaction_type = db.Column(db.Boolean)
