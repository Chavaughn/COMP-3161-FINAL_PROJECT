from app import app, db, hosturl
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, RegistrationForm
from werkzeug.security import check_password_hash
from app.controllers.AppController import *
from app.models import Account
import requests


# *****************Login form*****************
@app.route('/', methods=['POST', 'GET'])
def landing():
    if current_user.is_authenticated:
        # if user is already logged in, just redirect them to our secure page
        flash('User is already logged in.', 'info')
        return redirect(url_for('placeholder'))

    registration_form = RegistrationForm()
    login_form = LoginForm()
    # Login and validate the user.
    if login_form.validate_on_submit():
        if login_web(username=login_form.username.data, password=login_form.password.data) == 200:
            next_page = request.args.get('next')
            return redirect(next_page or url_for('placeholder'))
    flash_errors(login_form)
    return render_template('landing.html', lform = login_form, rform = registration_form)

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