from flask import jsonify, request
from app.controllers.AppController import *
from app.json_messages import *



@app.route('/course/student/register', methods=['POST'])
def add_student_to_course(lecturer_id):
    return ADDED_TO_COURSE_STUDENT