import User
from app import db
from flask import Flask

#for debugging 
app = Flask(__name__)
app.debug = True

#search model to be stored in analytics database 
class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    search_query = db.Column(db.String(200))
    search_result = db.Column(db.Text)

    #define relationship with user model
    user = db.relationship('User', backref = 'searches')

# if __name__ == '__main__':
#     app.run()