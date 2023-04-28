from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.json_messages import *

# *****************Get All Courses*****************
@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    courses = []
    with open('./app/sql/courses/getAllCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script)).all()
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name), student_count=course.students) for course in courses]
    return jsonify({"courses":courses}), 200

# *****************Get Courses that a student is enrolled in*****************
@app.route('/api/courses/student=<int:username>', methods=['GET'])
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
            courses = [dict(course_code=course.course_code, Course_Name=(course.course_name), Lecturer_id = course.lecturer_id, Lecturer_name = f"{course.first_name} {course.last_name}") for course in courses]
    return jsonify({"courses":courses}), 200

# *****************Get Courses that a lecturer does*****************
@app.route('/api/courses/lecturer=<int:lecturer_id>', methods=['GET'])
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
@app.route('/api/course/lecturer/add_lecturer=<int:lecturer_id>', methods=['PUT'])
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
@app.route('/api/course/members/<string:course_code>', methods=['GET'])
def get_course_members(course_code):
    members = []

    if course_exists(course_code):
        return COURSE_NOT_FOUND

    with open('./app/sql/courses/getCourseMembers.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_members = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    

    if course_members[0]:
        members = [{"id": member.account_id, "username": member.username,"name": member.first_name + ' ' + member.last_name, "email": member.email, "account_type": member.account_type} for member in course_members]
    return jsonify({"members": members})

# *****************Get Calendar Events Course*****************
@app.route('/api/course/events/<string:course_code>', methods=['GET'])
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
@app.route('/api/course/events/create', methods=['POST'])
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
@app.route('/api/course/forums/view/<string:course_code>', methods=['GET'])
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
@app.route('/api/course/forum/create', methods=['POST'])
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
@app.route('/api/course/forums/threads/view/<int:forum_id>', methods=['GET'])
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

    if threads:
        threads = [
             {
                'thread_id': thread.thread_id,
                'thread_title': thread.title,
                'message': thread.message,
                'Created By - account_id': thread.account_id,
             }
               for thread in threads]
    return jsonify({"Forum_id ": forum_id, "threads:": threads})


# *****************Add a new discussion thread to a forum*****************
@app.route('/api/course/forums/threads/new', methods=['POST'])
@login_required
def create_course_forum_thread():
    request_body = request.get_json()
    forum_id = request_body.get('forum_id')
    thread_title = request_body.get('thread_title')
    thread_message = request_body.get('thread_message')
    account_id = current_user.account_id

    with open('./app/sql/courses/forums/forumExists.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            forum_exists = db.session.execute(text(sql_script), {"forum_id": forum_id}).fetchone()

    if not forum_exists[0]:
        return FORUM_NOT_FOUND

    with open('./app/sql/courses/forums/newThread.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            db.session.execute(text(sql_script), {"forum_id": forum_id, "title": thread_title, "message": thread_message, "account_id": account_id})
            db.session.commit()
    
    return jsonify({"Forum_id ": forum_id, "Status ": "Successfully created thread"}), 201

# *****************Reply to a thread*****************
@app.route('/api/course/forums/threads/reply', methods=['POST'])
@login_required
def reply_to_thread():
    request_body = request.get_json()
    thread_id = request_body.get('thread_id')
    reply_title = request_body.get('reply_title')
    reply_message = request_body.get('reply_message')
    account_id = current_user.account_id
    parent_reply_id = request_body.get('parent_reply_id')
    initial_message = True if not parent_reply_id else False
    with open('./app/sql/courses/forums/threadExists.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            thread_exists = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchone()

    if not thread_exists[0]:
        return THREAD_NOT_FOUND

    with open('./app/sql/courses/forums/newReply.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            db.session.execute(text(sql_script), {"thread_id": thread_id, "title": reply_title, "message": reply_message,"initial_message": initial_message, "parent_reply_id":parent_reply_id, "account_id": account_id})
            db.session.commit()
    
    return jsonify({"Thread_id ": thread_id, "Status ": "Successfully created thread"}), 201


# *****************View all replies for a thread*****************
@app.route('/api/course/forums/threads/replies/<int:thread_id>', methods=['GET'])
def view_thread_replies(thread_id):
    replies = []

    with open('./app/sql/courses/forums/threadExists.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            thread_exists = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchone()

    if not thread_exists[0]:
        return THREAD_NOT_FOUND

    with open('./app/sql/courses/forums/getThread.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            thread = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchone()

    with open('./app/sql/courses/forums/getAllRepliesToThread.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            replies = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchall()
    if replies:
        if replies[0]:
            replies = [
                {
                    'thread_reply_id': reply.thread_reply_id,
                    'title': reply.title,
                    'message': reply.message,
                    'Created By - account_id': reply.account_id,
                    'initial_message': reply.initial_message,
                    'parent_reply_id': reply.parent_reply_id,
                }
                for reply in replies]
    return jsonify({"thread_a_id": thread_id,"thread_a_title": thread.title, "thread_aa_message": thread.message, "thread_replies": replies})


# *****************View all course content for a course*****************
@app.route('/api/course/content/<string:course_code>', methods=['GET'])
def get_course_content(course_code):
    content = []

    course_exists(course_code)

    with open('./app/sql/courses/content/getCourseContent.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_content = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()

    for row in course_content:
        urls = []
        if row.slide_link:
            urls.append({"Slide Name": row.slide_name, "Slide Link ": row.slide_link})
        if row.file_link:
            urls.append({"File Name": row.file_name, "File Link ": row.file_link})
        if row.link_link:
            urls.append({"Link Name": row.link_name, "Url": row.link_link})
        section_name = row.section_name
        if not content or content[-1]["section_name"] != section_name:
            section = {
                "section_name": section_name,
                "content": []
            }
            content.append(section)
        content[-1]["content"].append({
            "content_name": row.content_name,
            "content_description": row.content_description,
            "content_type": row.content_type if row.content_type else "Unspecified",
            "content_url": urls if urls else "No Links"
    })
    if content:
        return jsonify(content)
    return jsonify(f"No Content found in course: {course_code}")
    