from flask import jsonify, request
from app.controllers.AppController import *
from app.json_messages import *


# *****************Register Student to Course*****************
@app.route('/api/course/student/register', methods=['POST'])
def add_student_to_course(lecturer_id):
    return ADDED_TO_COURSE_STUDENT

# *****************Get Calendar Events for student for date*****************
@app.route('/api/student/<int:username>/calendar-events/<string:date>', methods=['GET'])
def get_student_calendar_events(username, date):
    events = []
    calendar_events = []
    student_exists(username)

    with open('./app/sql/students/events/getAllCalendarEventsForStudent.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            events = db.session.execute(text(sql_script), {"username": username, "event_date": date}).fetchall()
    if events:
        if events[0]:
            calendar_events = [
                {
                    'calendar_event_name': calendar_event.calendar_event_name,
                    'course_code': calendar_event.course_code,
                    'due_date': calendar_event.due_date.strftime('%A, %b %d, %Y'),
                    'given_date': calendar_event.given_date.strftime('%A, %b %d, %Y')
                }
                for calendar_event in events]
    else:
        calendar_events.append(
            {
            'No events for given period.': date
            }
        )
    return jsonify({"Username": username, "Calendar Events:": [calendar_events]}), 200

# *****************Get Student Grades*****************
@app.route('/api/student/<int:username>/grades', methods=['GET'])
def get_student_grades(username):
    student_grades = []
    student_name = ""
    scores = []
    final_average = 0

    student_exists(username)

    with open('./app/sql/students/grades/getGrades.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            grades = db.session.execute(text(sql_script), {"username": username}).fetchall()
    
    if not grades:
        return jsonify({f"Student with username: {username} has no grades to display"}), 404

    student_name = f"{grades[0].first_name} {grades[0].last_name}"

    for grade in grades:
        student_grades.append({
            "assignment_description" : grade.assignment_description,
            "course_code": grade.course_code,
            "grade": f"{grade.score}%"
        })
        scores.append(grade.score)
    
    final_average = calculate_final_average(scores)
    
    return jsonify({"Student": student_name,"Final Average": final_average, "Grades" : student_grades}), 200


def calculate_final_average(grades):
    total_score = sum(grades)
    num_grades = len(grades)
    final_average = total_score / num_grades if num_grades != 0 else 0
    
    return round(final_average, 2)