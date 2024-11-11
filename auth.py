#imports
from flask import redirect, render_template, request, session, url_for, Blueprint, flash
from db import db
from models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import re

#set up Blueprint
auth = Blueprint('auth', __name__)

# Function to validate email format
def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

#registration route 
@auth.route('/register', methods=['GET', 'POST'])
def register():
    already_user = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate email format
        if not is_valid_email(username):
            flash("Invalid email address. Please enter a valid email.", "error")
            return render_template('register.html', message="Invalid email address. Please enter a valid email.")

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exists, please go to Login page", "error")
            already_user = True
            return render_template('register.html', message="User already exists, please go to Login page")
        else:
            already_user = False

        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful", "success")
            return redirect(url_for('auth.login', message="Registration Successful", already_user=already_user))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred during registration. Please try again.", "error")
            return render_template('register.html', message="An error occurred during registration. Please try again.")

    return render_template('register.html', already_user=already_user, current_user=current_user)

#login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_failed = None
    login_attempted = False
    if request.method == 'POST':
        login_attempted = True
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            login_failed = True
            flash("Invalid username or password. Please try again.", "error")
        else:
            login_failed = False
            login_user(user)
            flash("Login Successful", "success")
            return redirect(url_for('index'))

    return render_template('login.html', login_failed=login_failed, login_attempted=login_attempted)

#logout route 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
