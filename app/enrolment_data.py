import csv
from datetime import datetime
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

print("***************Enrollments***************")
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

print("***************Calandar Events***************")
# Generate calendar events
calendar_events = []
for course_code in course_codes:
    for i in range(10):
        calendar_events.append({
            'due_date': f'2023-04-{random.randint(1,30):02d}',
            'given_date': datetime.now()
        })
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/calendar_events.csv', mode='w', newline='') as csv_file:
    fieldnames = [ 'due_date', 'given_date'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for event in calendar_events:
        writer.writerow(event)
print("***************Forums***************")
# Generate forum posts
forum_posts = []
for course_code in course_codes:
    forum_posts.append({
        'course_code': course_code
    })
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/forum_posts.csv', mode='w', newline='') as csv_file:
    fieldnames = ['course_code'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for forum in forum_posts:
        writer.writerow(forum)


print("***************Threads***************")
# Generate discussion threads
discussion_threads = []
i=0
for course_code in course_codes:
    discussion_threads.append({
        'forum_id': i+1,
        'title': f'Discussion thread for course {course_code}',
        'message': 'This is the first post in the discussion thread.',
        'initial_message': 1,
        'account_id': random.randint(1,100000)
    })
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/threads.csv', mode='w', newline='') as csv_file:
    fieldnames = ['forum_id', 'title', 'message', 'initial_message', 'account_id'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for discussion_thread in discussion_threads:
        writer.writerow(discussion_thread)

print("***************Thread Reply***************")
# Generate replies to discussion threads
replies = []
i=0
x=0
for discussion_thread in discussion_threads:
    i+1
    for i in range(random.randint(1,10)):
        x+1
        replies.append({
            'thread_id': i,
            'title': f'Discussion thread reply for thread',
            'message': f'Reply {i} to the discussion thread.',
            'initial_message': 0,
            'account_id': random.randint(1,100000)
        })
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/thread_replies.csv', mode='w', newline='') as csv_file:
    fieldnames = ['thread_id', 'title', 'message', 'initial_message', 'account_id'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for reply in replies:
        writer.writerow(reply)



# Generate course content
# course_content = []
# for course_code in course_codes:
#     for section in range(1, 5):
#         course_content.append({
#             'course_code': course_code,
#             'section': section,
#             'title': f'Section {section} for course {course_code}',
#             'content': 'This is the content for this section.'
#         })

# Generate assignments
# assignments = []
# for course_code in course_codes:
#     for i in range(10):
#         assignments.append({
#             'course_code': course_code,
#             'title': f'Assignment {i+1} for course {course_code}',
#             'description': 'This is the description for this assignment.',
#             'due_date': f'2023-05-{random.randint(1,30):02d}'
#         })

# Generate grades
# grades = []
# for student_id in student_ids:
#     for assignment in assignments:
#         if random.random() < 0.8:
#             grade = random.randint(50,100)
#             grades.append({
#                 'student_id': student_id,
#                 'assignment_id': None,
#                 'course_code': assignment['course_code'],
#                 'grade': grade
#             })