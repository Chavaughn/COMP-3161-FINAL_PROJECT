from functools import wraps

from sqlalchemy import text
from app import app, db, login_manager, hosturl
from flask import jsonify, make_response, redirect, render_template, url_for, flash
from flask_login import UserMixin, current_user
from app.json_messages import UNAUTHORIZED

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

@app.route('/placeholder')
def placeholder():
    """Custom 404 page."""
   #print(current_user.account_id)
    return render_template('404.html')


def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('landing'))
        return f(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(id):
    #  with open('./app/sql/load_user.sql', 'r') as file:
    #     sql_script = file.read()
    user = db.session.execute(db.select(Account).filter_by(account_id=id)).scalar()
    return user

# Handle login required error
@app.errorhandler(401)
def unauthorized(error):
    response = make_response(UNAUTHORIZED)
    response.headers['Content-Type'] = 'application/json'
    return response