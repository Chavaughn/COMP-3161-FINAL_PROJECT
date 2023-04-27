from datetime import datetime
from flask import jsonify, request
from flask_login import *
from app.controllers.AppController import *
from app.json_messages import *


@app.route('/api/reports/highest_performing_students', methods=['GET'])
def highest_performing_students_report():
    performers = []
    with open('./app/sql/reports/highestPerformingStudents.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            students = db.session.execute(text(sql_script)).fetchall()
    place = 1
    for student in students:
        performers.append({
            "position": place,
            "student_id": student.student_id,
            "username": student.username,
            "name": f"{student.first_name} {student.last_name}",
            "final_average": round(student.final_average, 2)
        })
        place = place +1
    return jsonify(performers)

@app.route('/api/reports/most_enrolled_courses', methods=['GET'])
def most_Enrolled_Courses():
    with open('./app/sql/reports/mostEnrolledCourses.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            courses = db.session.execute(text(sql_script)).fetchall()

    return jsonify([{"course_code": course.course_code, "course_name": course.course_name, "student_count": course.student_count} for course in courses])

@app.route('/api/reports/course_loaded_lecturers', methods=['GET'])
def course_loaded_lecturers():
    with open('./app/sql/reports/courseLoadedLecturers.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            lecturers = db.session.execute(text(sql_script)).fetchall()

    return jsonify([{"lecturer_name": f"{lecturer.first_name} {lecturer.last_name}", "username": lecturer.username, "courses_taught": lecturer.course_count, "lecturer_id": lecturer.lecturer_id} for lecturer in lecturers])

@app.route('/api/reports/work_a_holic_students', methods=['GET'])
def work_a_holic_students():
    sardines = []
    with open('./app/sql/reports/courseLoadedStudents.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            students = db.session.execute(text(sql_script)).fetchall()

    return jsonify([{"student_name": f"{student.first_name} {student.last_name}", "username": student.username, "courses_enrolled": student.course_count, "student_id": student.student_id} for student in students])


@app.route('/api/reports/packed_courses', methods=['GET'])
def sardine_courses():
    with open('./app/sql/reports/seatedCourses.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            courses = db.session.execute(text(sql_script)).fetchall()

    return jsonify([{"course_code": course.course_code, "course_name": course.course_name, "student_count" : course.student_count} for course in courses])


@app.route('/api/profile')
def profile():
    return render_template('test.html')

@app.route('/api/course')
def course():
    return render_template('course.html')

@app.route('/api/forum')
def forum():
    return render_template('forum.html')





