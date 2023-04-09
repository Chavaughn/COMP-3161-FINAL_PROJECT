from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.json_messages import *

# *****************Get All Courses*****************
@app.route('/courses', methods=['GET'])
def get_all_courses():
    courses = []
    with open('./app/sql/courses/getAllCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script)).all()
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name)) for course in courses]
    return jsonify({"courses":courses}), 200

# *****************Get Courses that a student is enrolled in*****************
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

# *****************Get Courses that a lecturer does*****************
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

# *****************Add a lecturer to a course*****************
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

# *****************Get Members of a Course*****************
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

# *****************Get Calendar Events Course*****************
@app.route('/course/events/<string:course_code>', methods=['GET'])
def get_course_calendar_events(course_code):
    events = []

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND

    with open('./app/sql/courses/events/getAllCalendarEventsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            events = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    
    if events[0]:
        calendar_events = [
             {
                'calendar_event_name': calendar_event.calendar_event_name,
                'due_date': calendar_event.due_date.strftime('%A, %b %d, %Y'),
                'given_date': calendar_event.given_date.strftime('%A, %b %d, %Y')
             }
               for calendar_event in events]
    return jsonify({"Course ": course_code, "Calendar Events:": calendar_events})

# *****************Create Calendar Event for a Course*****************
@app.route('/course/events/create', methods=['POST'])
@login_required
def create_course_calendar_event():
    data = request.json
    course_code = data['course_code']
    calendar_event_name = data['calendar_event_name']
    given_date = data['given_date']
    due_date = data['due_date']

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND
    
    with open('./app/sql/courses/events/newCalendarEvent.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            db.session.execute(text(sql_script), 
                                                {
                                                    "course_code": course_code,
                                                    "calendar_event_name": calendar_event_name,
                                                    "given_date": given_date,
                                                    "due_date":due_date
                                                })
            db.session.commit()
            
    return CALENDAR_EVENT_CREATED
    

# *****************View Forum for course*****************
@app.route('/course/forums/view/<string:course_code>', methods=['GET'])
def view_course_forum(course_code):
    forums = []

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND
            
    with open('./app/sql/courses/forums/getAllForumsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            forums = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    
    if forums[0]:
        forums = [
             {
                'forum_id': forum.forum_id,
                'forum_name': forum.forum_name
             }
               for forum in forums]
    return jsonify({"Course ": course_code, "Forums:": forums})


# *****************Create Forum for a Course*****************
@app.route('/course/forum/create', methods=['POST'])
@login_required
def create_course_forum():
    data = request.json
    course_code = data['course_code']
    forum_name = data['forum_name']

    with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

    if not course_exists[0]:
        return COURSE_NOT_FOUND
    
    with open('./app/sql/courses/forums/newForum.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            db.session.execute(text(sql_script), 
                                                {
                                                    "course_code": course_code,
                                                    "forum_name": forum_name,
                                                })
            db.session.commit()
            
    return FORUM_CREATED

# *****************View all threads for forum*****************
@app.route('/course/forums/threads/view/<int:forum_id>', methods=['GET'])
def view_course_forum_threads(forum_id):
    threads = []

    with open('./app/sql/courses/forums/forumExists.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            forum_exists = db.session.execute(text(sql_script), {"forum_id": forum_id}).fetchone()

    if not forum_exists[0]:
        return FORUM_NOT_FOUND
            
    with open('./app/sql/courses/forums/getAllThreadsForForum.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            threads = db.session.execute(text(sql_script), {"forum_id": forum_id}).fetchall()

    if threads[0]:
        threads = [
             {
                'thread_id': thread.thread_id,
                'thread_title': thread.title,
                'message': thread.message,
                'Created By - account_id': thread.account_id,
             }
               for thread in threads]
    return jsonify({"Forum_id ": forum_id, "threads:": threads})