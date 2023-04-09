from flask import jsonify, request
from app.controllers.AppController import *
from app.json_messages import *


# *****************Register Student to Course*****************
@app.route('/course/student/register', methods=['POST'])
def add_student_to_course(lecturer_id):
    return ADDED_TO_COURSE_STUDENT

# *****************Get Calendar Events for student for date*****************
@app.route('/student/<int:username>/calendar-events/<string:date>', methods=['GET'])
def get_student_calendar_events(username, date):
    events = []
    calendar_events = []
    with open('./app/sql/students/checkStudentExistence.sql', 'r') as file:
        sql_script = file.read()
        with app.app_context():
            student_exists = db.session.execute(text(sql_script), {"username": username}).fetchone()

    if not student_exists[0]:
        return STUDENT_NOT_FOUND

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
    return jsonify({"Username": username, "Calendar Events:": [calendar_events]})