#GENERAL
from flask import jsonify
from app import app

with app.app_context():
    ACTION_NOT_ALLOWED = jsonify({"message": "Current action not allowed"}), 401
    INVALID_REGISTRATION = jsonify({"message": "Invalid registration"}), 401
    COURSE_CREATED = jsonify({"message": "Course Created"}), 200
    ADDED_TO_COURSE_LECTURER = jsonify({"message": "Lecturer added to course"}), 200
    ADDED_TO_COURSE_STUDENT = jsonify({"message": "Student registered for course"}), 200
    LECTURER_TOO_MANY = jsonify({"message": "Lecturer is already teaching 5 courses!"}), 401
    COURSE_NOT_FOUND = jsonify({"error": "Course not found"}), 404