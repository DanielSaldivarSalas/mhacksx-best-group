from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class ProfileInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    picture = db.Column(db.BLOB)

class GameInfo(db.Model):
    round_id = db.Column(db.Integer, primary_key = True)
    round_time = db.Column(db.DateTime, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    
