from models import User
from db import db

#search model to be stored in analytics database 
class Search(db.Model):
    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    search_query = db.Column(db.String(200))
    search_result = db.Column(db.Text)

    #define relationship with user model
    user = db.relationship('User', backref = 'searches')