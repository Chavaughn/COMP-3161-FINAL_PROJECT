import csv
import random
from sqlalchemy import text
from app import app, db

with open('./app/sql/students/getAllStudent_Ids.sql', 'r') as file:
    sql_script = file.read()
    with app.app_context():
        students = db.session.execute(text(sql_script))

with open('./app/sql/courses/getAllCourseCodes.sql', 'r') as file:
    sql_script = file.read()
    with app.app_context():
        courses = db.session.execute(text(sql_script))

# Convert the results to lists of student IDs and course codes
#print(students.all()[100000-1][0])
student_ids = []
course_codes = []
student_query = students.all()
course_query = courses.all()

for i in range(len(student_query)):
    student_id = student_query[i][0]
    student_ids.append((student_id))

for i in range(len(course_query)):
    course_code = course_query[i][0]
    course_codes.append((course_code))

course_count = {}
student_count = {}

# Initialize the count for each course to 0
for course_code in course_codes:
    course_count[course_code] = 0

# Initialize the count for each student to 0
for student_id in student_ids:
    student_count[student_id] = 0



with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/enrollments.csv', mode='w', newline='') as csv_file:
    fieldnames = ['student_id', 'course_code']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()
    rows = []
    # Generate enrollments for each student
    a = len(student_ids)
    b = len(course_codes)
    for student_id in student_ids:
        # Choose a random number of courses between 3 and 6
        num_courses = random.randint(3, 6)

        # Choose courses for the student
        chosen_courses = []
        while len(chosen_courses) < num_courses:
            course_code = random.choice(course_codes)
            course_count[course_code] += 1  # increment the count for the course
            if course_count[course_code] <= 10:  # check if the count is less than or equal to 10
                chosen_courses.append(course_code)
            else:
                chosen_courses.append(random.choice(course_codes))
            #print(f"k:{k}")
        # Increment the count for the chosen courses and student
        for course_code in chosen_courses:
            student_count[student_id] += 1

        # Write the enrollment to the CSV file
        student_rows = [{'student_id': student_id, 'course_code': course_code.strip()} for course_code in chosen_courses]
        writer.writerows(student_rows)

