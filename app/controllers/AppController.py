from functools import wraps

from sqlalchemy import text
from app import app, db, login_manager, hosturl
from flask import jsonify, make_response, redirect, render_template, url_for, flash
from flask_login import UserMixin, current_user
from app.json_messages import *

from app.models import Account


def course_exists(course_code):
    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return True
    return False

def student_exists(username):
    with open('./app/sql/students/checkStudentExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            student_exists = db.session.execute(text(sql_script), {"username": username}).fetchone()

    if not student_exists[0]:
        return True
    return False
    

def student_course_count_check(student_id):
    with open('./app/sql/students/checkStudentCourseAmount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_count = db.session.execute(text(sql_script), {"student_id": student_id}).fetchone()
    if course_count.course_count >= 6:
        return True
    return False
    

def get_account(username):
    with open('./app/sql/accounts/getAccount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            account = db.session.execute(text(sql_script), {"username": username}).fetchone()
    return account

def student_in_course_check(student_id, course_code):
    with open('./app/sql/students/checkStudentAlreadyInCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_count = db.session.execute(text(sql_script), {"student_id": student_id, "course_code": course_code}).fetchone()
    if course_count:
        return True
    return False

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
            return redirect(url_for('home'))
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