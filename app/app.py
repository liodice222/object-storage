from flask import Flask
from models import db
from dotenv import load_dotenv
import os
from main.routes import main as main_blueprint
from flask_login import LoginManager
from models.User import User
from models import db 


load_dotenv()

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(main_blueprint)


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#debugging for secret key 
#print(f"Secret Key: {app.config['SECRET_KEY']}")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)