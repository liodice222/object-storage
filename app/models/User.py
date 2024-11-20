from flask_login import UserMixin
from . import db

#set up user model to be stored in user database  
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    searches = db.relationship('Search', backref='user', lazy=True)

