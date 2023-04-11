from functools import wraps

from sqlalchemy import text
from app import app, db, login_manager, hosturl
from flask import jsonify, redirect, render_template, url_for, flash
from flask_login import UserMixin, current_user

from app.models import Account




# === Flash functionality ===
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')
# ...


@app.route('/profile')
def profile():
    return render_template('test.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/course')
def course():
    return render_template('course.html')

@app.route('/forum')
def forum():
    return render_template('forum.html')





