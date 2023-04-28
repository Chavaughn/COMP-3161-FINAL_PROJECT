from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.forms import AddCourseForm, CreateCalendarEventForm, LoginForm, RegisterForCourseForm, RegistrationForm
from app.json_messages import *
from werkzeug.security import check_password_hash, generate_password_hash



@app.route("/login", methods = ['POST', 'GET'])
@logout_required
def login():
    form = LoginForm()
    if form.validate_on_submit() and request.method == "POST":
        username = form.username.data
        password = form.password.data
        user = Account.query.filter_by(username=username).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Username or Password is incorrect.', 'danger')
    return render_template('login.html', form=form)

@app.route("/fr/register", methods = ['POST', 'GET'])
def registration_view():
    if current_user.is_authenticated:
        flash('User is already logged in.', 'info')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        account_type = request.form.get('account_type')
        with open('./app/sql/students/getLastUsername.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                last_username = db.session.execute(text(sql_script)).first()[0]
        username = last_username + 1
        email = f"{username}@mymona.uwi.edu"
        with open('./app/sql/accounts/registerAccount.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script),  
                                    {
                                "username": username,
                                "first_name":first_name,
                                "last_name":last_name,
                                "password": password,
                                "email":email,
                                "account_type":account_type
                            })
                db.session.commit()
        with open('./app/sql/accounts/getAccount.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                user = db.session.execute(text(sql_script),  {"username": username}).first()
        if (account_type == '2'):
            #register lecturer
            with open('./app/sql/lecturers/registerLecturer.sql', 'r') as file:
                sql_script = file.read()
                with app.app_context():
                    db.session.execute(text(sql_script), {"account_id": user[0]})
                    db.session.commit()
            flash('Registered! - Lecturer', 'success')
            return redirect(url_for('home'))
        elif(account_type == '3'):
            #register student
            print("student")
            with open('./app/sql/students/registerStudent.sql', 'r') as file:
                sql_script = file.read()
                with app.app_context():
                    db.session.execute(text(sql_script), {"account_id": user[0]})
                    db.session.commit()
            flash('Registered! - Student', 'success')
            return redirect(url_for('home'))
    return render_template('signup.html', form=form)

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
    account = get_account(current_user.username)
    with open('./app/sql/courses/getStudentCourses.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            student_courses = db.session.execute(text(sql_script), {"student_id": account.student_id})
    for course in student_courses:
        course_information[0]['Courses'].append(get_course_information(course.course_code))
    if current_user.account_type == 1:
        with open('./app/sql/courses/getAllCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script)).all()
        return render_template('adminhome.html', courses = courses)
    elif current_user.account_type == 2:
        with open('./app/sql/courses/getLecturerCourses.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                courses = db.session.execute(text(sql_script), {"lecturer_id":account.lecturer_id} ).all()
        return render_template('lecturerhome.html', courses = courses)
    elif current_user.account_type == 3:
        return render_template('home.html', courses = course_information[0]['Courses'])


@app.route("/fr/course/<string:course_code>", methods=['GET'])
@login_required
def course_view(course_code):
    course_information = get_course_information(course_code)
    sections = get_sections_for_course(course_code)
    forums = get_forum_information_for_course(course_code)
    assignments = get_assignments_for_course(course_code)
    calendar_events = get_calendar_events(course_code)
    return render_template('course.html',
                            course = course_information,
                            sections = sections,
                            forums = forums,
                            assignments = assignments,
                            calendar_events = calendar_events)

@app.route('/fr/course/events/create', methods=['GET','POST'])
@login_required
def create_calendar_event():
    form = CreateCalendarEventForm()
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        calendar_event_name = request.form.get('calendar_event_name')
        due_date = request.form.get('due_date')

        with open('./app/sql/courses/events/newCalendarEvent.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), 
                                                    {
                                                        "course_code": course_code,
                                                        "calendar_event_name": calendar_event_name,
                                                        "given_date": datetime.now(),
                                                        "due_date":due_date
                                                    })
                db.session.commit()
        flash("Calendar Event successfully created", "success")
        return redirect(url_for('course_view', course_code=course_code))
    with open('./app/sql/courses/getAllCourseCodes.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            courses = db.session.execute(text(sql_script)).fetchall()
    return render_template("createcalendarevent.html", form = form, courses = courses)

@app.route("/fr/course/register/username=<int:username>", methods=['GET', 'POST'])
@login_required
def register_for_course_view(username):
    form = RegisterForCourseForm()
    if request.method == 'POST':
        course_code = request.form.get('course_select')
        account = get_account(username)
        if student_exists(username):
            flash('Student not found', 'danger')
            return redirect(url_for('register_for_course_view', username=username))
        if student_course_count_check(account.student_id):
            flash('Already doing max amount of courses', 'danger')
            return redirect(url_for('register_for_course_view', username=username))
        if course_exists(course_code):
            flash('Course does not exist', 'danger')
            return redirect(url_for('register_for_course_view', username=username))
        if student_in_course_check(account.student_id, course_code):
            flash('Student Already in course', 'danger')
            return redirect(url_for('register_for_course_view', username=username))
        with open('./app/sql/students/registerForCourseStudent.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), {"course_code": course_code, "student_id": account.student_id})
                db.session.commit()
        flash('Registered for course.', 'success')
        return redirect(url_for('home'))
    with open('./app/sql/courses/getAllCourseCodes.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            courses = db.session.execute(text(sql_script)).fetchall()
    return render_template('register_for_course_student.html', form=form, courses=courses)

@app.route("/fr/course/add", methods=['GET','POST'])
@login_required
def add_course_view():
    form = AddCourseForm()
    if current_user.account_type != 1:
        return redirect(url_for("home"))
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_title = request.form.get('course_title')
        course_description = request.form.get('course_description')
        with open('./app/sql/courses/checkCourseExistence.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                course_exists = db.session.execute(text(sql_script), {"course_code": course_code}).fetchone()

        if course_exists[0]:
            flash('Course code Exists', 'danger')
            return redirect(url_for("add_course_view"))

        with open('./app/sql/courses/addCourse.sql', 'r') as file:
            sql_script = file.read()
            with app.app_context():
                db.session.execute(text(sql_script), {"course_code": course_code, "course_title": course_title, "course_description":course_description})
                db.session.commit()
            flash('Course Created', 'success')
            return redirect(url_for('home'))
    return render_template('addcourseformview.html', form=form)


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

def get_calendar_events(course_code):
    with open('./app/sql/courses/events/getAllCalendarEventsForCourse.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            events = db.session.execute(text(sql_script), {"course_code": course_code}).fetchall()
    return events if events else None