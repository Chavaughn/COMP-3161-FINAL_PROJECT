#GENERAL
from flask import jsonify
from app import app

with app.app_context():
    ACTION_NOT_ALLOWED = jsonify({"message": "Current action not allowed"}), 401
    INVALID_REGISTRATION = jsonify({"message": "Invalid registration"}), 401
    UNAUTHORIZED = jsonify({'message': 'Unauthorized. Please log in.'}), 401

    COURSE_CREATED = jsonify({"message": "Course Created"}), 200
    ADDED_TO_COURSE_LECTURER = jsonify({"message": "Lecturer added to course"}), 200
    ADDED_TO_COURSE_STUDENT = jsonify({"message": "Student registered for course"}), 200
    LECTURER_TOO_MANY = jsonify({"message": "Lecturer is already teaching 5 courses!"}), 401
    STUDENT_DOES_MAX = jsonify({"message": "Student is already enrolled in 6 courses!"}), 401
    STUDENT_IN_COURSE = jsonify({"message": "Student is already enrolled in course!"}), 401
    COURSE_EXISTS_ALREADY = jsonify({"message": "Course already exists"}), 401

    CALENDAR_EVENT_CREATED = jsonify({"message": "Calendar event created successfully."}), 201
    FORUM_CREATED = jsonify({"message": "Forum event created successfully."}), 201

    COURSE_NOT_FOUND = jsonify({"error": "Course not found"}), 404
    THREAD_NOT_FOUND = jsonify({"error": "Thread not found"}), 404
    STUDENT_NOT_FOUND = jsonify({"error": "Student not found"}), 404
    FORUM_NOT_FOUND = jsonify({"error": "Forum not found"}), 404