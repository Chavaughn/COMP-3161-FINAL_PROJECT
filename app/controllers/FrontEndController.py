from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.forms import LoginForm
from app.json_messages import *
from werkzeug.security import check_password_hash



@app.route("/login", methods = ['POST', 'GET'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        username = form.username.data
        password = form.password.data
        print(password)
        user = Account.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully.', 'success')
            return render_template('home.html')
        else:
            flash('Username or Password is incorrect.', 'danger')
    return render_template('login.html', form=form)


@app.route("/logout_current_user", methods = ['GET'])
@login_required
def frontend_logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('landing'))


@app.route("/home")
@login_required
def home():
    course_information = [{"Courses": []}]
    with open('./app/sql/courses/getStudentCourses.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            student_courses = db.session.execute(text(sql_script), {"student_id": current_user.account_id})
    for course in student_courses:
        course_information[0]['Courses'].append(get_course_information(course.course_code))
    return render_template('home.html', courses = course_information[0]['Courses'])


@app.route("/fr/course/<string:course_code>")
@login_required
def course_view(course_code):
    course_information = get_course_information(course_code)
    sections = get_sections_for_course(course_code)
    forums = get_forum_information_for_course(course_code)
    assignments = get_assignments_for_course(course_code)
    return render_template('course.html',
                            course = course_information,
                              sections = sections,
                                forums = forums,
                                assignments = assignments)

@app.route("/fr/course/<string:course_code>/forum=<int:forum_id>")
@login_required
def forum_view(course_code, forum_id):
    with open('./app/sql/courses/forums/getAllForumsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            forums = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    for forum in forums:
        if forum.forum_id == forum_id:
            fourm = forum

    with open('./app/sql/courses/forums/getAllThreadsForForum.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            threads = db.session.execute(text(sql_script), {"forum_id": forum_id}).fetchall()
    return render_template('forum.html', forum = forum, threads = threads)

@app.route("/fr/course/forum=<int:forum_id>/thread=<int:thread_id>")
@login_required
def thread_view(forum_id, thread_id):
    with open('./app/sql/courses/forums/getThread.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            thread = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchone()
    with open('./app/sql/courses/forums/getAllRepliesToThread.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            replies = db.session.execute(text(sql_script), {"thread_id": thread_id}).fetchall()
    return render_template('thread.html', thread = thread, replies = replies)


@app.route("/fr/course/assignment=<int:assignment_id>/<string:course_code>")
@login_required
def assignment_view(assignment_id, course_code):
    assignment = get_assignment(assignment_id)
    print(assignment)
    return render_template('assignment.html', assignment = assignment, course_code = course_code)


def get_course_information(course_code):
    with open('./app/sql/frontend/getCourseInformation.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            course_information = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()
    return course_information


def get_sections_for_course(course_code):
    content = []
    with open('./app/sql/courses/content/getCourseContent.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            section_information = db.session.execute(text(sql_script), {"course_code": course_code})
    section_dict = {}
    for row in section_information:
        section_name = row.section_name
        if section_name not in section_dict:
            section_dict[section_name] = {"section_name": section_name, "content": []}
        urls = []
        if row.slide_link:
            urls.append({"name": row.slide_name, "link": row.slide_link})
        if row.file_link:
            urls.append({"name": row.file_name, "link": row.file_link})
        if row.link_link:
            urls.append({"name": row.link_name, "link": row.link_link})
        section_dict[section_name]["content"].append({
            "content_name": row.content_name,
            "content_description": row.content_description,
            "content_url": urls if urls else "No Links"
        })

    content = list(section_dict.values())
    return content        

def get_forum_information_for_course(course_code):
    with open('./app/sql/courses/forums/getAllForumsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            forums = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    return forums

def get_assignments_for_course(course_code):
    with open('./app/sql/frontend/getAssignmentsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            assignments = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    return assignments

def get_assignment(assignment_id):
    with open('./app/sql/frontend/getCurrentUser.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            user = db.session.execute(text(sql_script), {"account_id": current_user.account_id}).fetchone()
    print(user)
    with open('./app/sql/frontend/getAssignmentForStudent.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            assignment = db.session.execute(text(sql_script), {"assignment_id": assignment_id, "student_id": user.student_id}).fetchone()
    return assignment