from app import app
from app.models import db
from app.main import routes
from app.models import User

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)