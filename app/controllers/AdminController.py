from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.json_messages import *

@app.route('/api/admin/course/add_course', methods=['POST'])
def add_Course():
    if current_user.is_authenticated():
        if current_user.account_type != 1:
            return ACTION_NOT_ALLOWED
    course_code = request.json['course_code']
    course_title = request.json['course_title']
    course_description = request.json['course_description']
    lecturer_id = request.json['course_lecturer']
    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
             course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if course_exists[0]:
        return COURSE_EXISTS_ALREADY

    with open('./app/sql/courses/addCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            db.session.execute(text(sql_script), {"course_code": course_code, "course_title": course_title, "course_description":course_description ,"lecturer_id": lecturer_id})
            db.session.commit()
    return COURSE_CREATED