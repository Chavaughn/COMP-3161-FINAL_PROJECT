from app import app, db, hosturl
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *
from app.models import Account
import requests


# *****************Login form*****************
@app.route('/')
@logout_required
def landing():
    
    return render_template('landing.html')

# *****************Login 2*****************
@app.route('/loginw', methods=['POST'])
@logout_required
def login_web(username, password):
    user = Account.query.filter_by(username=username).first()
    if user is not None and check_password_hash(user.password, password):
        login_user(user, remember=True)
        flash('Logged in successfully.', 'success')
        return 200
    else:
        flash('Username or Password is incorrect.', 'danger')

# *****************Login 1*****************
@app.route('/api/login', methods=['POST'])
@logout_required
def login_postman():
    username = request.json['username']
    password = request.json['password']
    user = Account.query.filter_by(username=username).first()
    if user is not None and check_password_hash(user.password, password):
        login_user(user, remember=False)
        return jsonify({"message": "Logged in successfully."},{"username":current_user.username}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401

# *****************Logout*****************
@app.route("/logout")
@login_required
def logout_user_api():
    logout_user()
    return jsonify({"message": "Logged out successfully."}), 200
# ...