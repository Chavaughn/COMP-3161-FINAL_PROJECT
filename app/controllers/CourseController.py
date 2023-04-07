from flask import jsonify, request
from app.controllers.AppController import *
from app.json_messages import *


@app.route('/courses', methods=['GET'])
def get_all_courses():
    courses = []
    with open('./app/sql/courses/getAllCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script)).all()
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name)) for course in courses]
    return jsonify({"courses":courses}), 200

@app.route('/courses/student=<int:username>', methods=['GET'])
def get_student_courses(username):
    courses = []
    with open('./app/sql/accounts/getAccount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
             user = db.session.execute(text(sql_script),  {"username": username}).first()
    with open('./app/sql/students/getStudentFromAccountId.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
             student = db.session.execute(text(sql_script),  {"account_id": user[0]}).first()
    with open('./app/sql/courses/getStudentCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script), {"student_id":student[0]} ).all()
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name)) for course in courses]
    return jsonify({"courses":courses}), 200


@app.route('/courses/lecturer=<int:lecturer_id>', methods=['GET'])
def get_lecturer_courses(lecturer_id):
    courses = []
    # with open('./app/sql/lecturers/getLecturerAccount.sql', 'r') as file:
    #         sql_script = file.read()
    #         with app.app_context():
    #             lecturer_account = db.session.execute(text(sql_script), {"lecturer_id":lecturer_id} ).all()
            
    with open('./app/sql/courses/getLecturerCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script), {"lecturer_id":lecturer_id} ).all()
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name)) for course in courses]
    return jsonify({"courses":courses}), 200

@app.route('/course/lecturer/add_lecturer=<int:lecturer_id>', methods=['PUT'])
def add_lecturer_course(lecturer_id):
    course_code = request.json['course_code']
    with open('./app/sql/lecturers/getLecturerAccount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            lecturer_account = db.session.execute(text(sql_script), {"lecturer_id": lecturer_id} ).all()
    if lecturer_account[0].account_type != 2:
         return ACTION_NOT_ALLOWED
    
    with open('./app/sql/lecturers/getLecturerCourseAmount.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_amount = db.session.execute(text(sql_script), {"lecturer_id": lecturer_id}).fetchone()

    if course_amount[0] >= 5:
         return LECTURER_TOO_MANY

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND

    with open('./app/sql/courses/updateCourseLecturer.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), {"lecturer_id":lecturer_id, "course_code":course_code } )
                db.session.commit()
    return ADDED_TO_COURSE_LECTURER



@app.route('/course/members/<string:course_code>', methods=['GET'])
def get_course_members(course_code):
    members = []

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND

    with open('./app/sql/courses/getCourseMembers.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_members = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    

    if course_members[0]:
        members = [{"id": member.account_id, "username": member.username,"name": member.first_name + ' ' + member.last_name, "email": member.email, "account_type": member.account_type} for member in course_members]
    return jsonify({"members": members})
