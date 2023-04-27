from collections import defaultdict
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
student_ids = [student[0] for student in students.fetchall()]
course_codes = [course[0] for course in courses.fetchall()]

# Initialize course and student counters
course_count = {course_code: 0 for course_code in course_codes}
student_count = {student_id: 0 for student_id in student_ids}

# Initialize the count for each course to 0
for course_code in course_codes:
    course_count[course_code] = 0

# Initialize the count for each student to 0
for student_id in student_ids:
    student_count[student_id] = 0
student_rows = []
student_enrollment_data = {}

print("***************Enrollments***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/enrollments.csv', mode='w', newline='') as csv_file:
    fieldnames = ['student_id', 'course_code']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()
    student_rows = []
    # Initialize a set to store all the previous enrollments
    enrollments_set = set()
    # Generate enrollments for each student
    a = len(student_ids)
    b = len(course_codes)
    for student_id in student_ids:
        # Choose a random number of courses between 3 and 6
        num_courses = random.randint(3, 6)

        # Choose courses for the student
        chosen_courses = []
        student_enrollment_data.setdefault(student_id, {'courses': []})
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
        for course_code in chosen_courses:
            # Check if the current enrollment already exists in the set
            enrollment = (student_id, course_code.strip())
            if enrollment not in enrollments_set:
                student_rows.append({'student_id': student_id, 'course_code': course_code.strip()})
                enrollments_set.add(enrollment)
                # Find the dictionary for the current student
                enrollment_data = student_enrollment_data[student_id]
                # Get the list of courses and append the course data
                courses_list = enrollment_data['courses']
                courses_list.append({'course_code': course_code.strip()})
                enrollment_data['courses'] = courses_list
    writer.writerows(student_rows)

print("Checkpoint 1")
# Generate calendar events
calendar_events = []
forum_posts = []
discussion_threads = []
events = []
sections = []
course_content = []
# Create a dictionary to store the assignments for each course
course_assignments = {course_code.strip(): [] for course_code in course_codes}
course_events = {course_code.strip(): [] for course_code in course_codes}
# Generate a list of assignments for each course
assignments = []
x=0
b = 0
ce_id=1
for course_code in course_codes:
    b = b+1
    sections.append({ 'section_name': 'Section 1','course_code': course_code.strip()})
    sections.append({ 'section_name': 'Section 2','course_code': course_code.strip()})
    sections.append({ 'section_name': 'Mid-Term Exam','course_code': course_code.strip()})
    sections.append({ 'section_name': 'Section 3','course_code': course_code.strip()})
    sections.append({ 'section_name': 'Final Exam','course_code': course_code.strip()})
    for i in range(10):
        event = {
            'calendar_event_id': ce_id,
            'course_code': course_code.strip(),
            'calendar_event_name': f'Event: {i} for Course: {course_code}',
            'due_date': f'2023-05-{random.randint(1,30):02d}',
            'given_date': datetime.now()
        }
        calendar_events.append({
            'course_code': course_code.strip(),
            'calendar_event_name': f'Event: {i} for Course: {course_code}',
            'due_date': f'2023-05-{random.randint(1,30):02d}',
            'given_date': datetime.now()
        })
        ce_id = ce_id+1
        course_events[course_code.strip()].append(event['calendar_event_id'])
    forum_posts.append({
        'course_code': course_code.strip(),
        'forum_name': f"Fourm for {course_code}"
    })
    discussion_threads.append({
        'title': f'Discussion thread for course {course_code.strip()}',
        'forum_id': x+1,
        'message': 'This is the first post in the discussion thread.',
        'account_id': random.randint(1,100000)
    })
    x = x+1

print("Checkpoint 2")
replies = []
i=0
for discussion_thread in discussion_threads:
    i = i+1
    x=0
    for o in range(random.randint(1,10)):
        x=x+1
        replies.append({
            'title': f'Discussion thread reply for thread',
            'thread_id': i,
            'message': f'Reply {x} to the discussion thread.',
            'initial_message': 1,
            'account_id': random.randint(1,100000)
        })

print("Checkpoint 3")
c = 0
b = 1
for course_code in course_codes:
    course_events_list = course_events[course_code.strip()]
    for j in range(1, 6):
        c = c + 1
        random_event_id = random.choice(course_events_list)
        if j <= 3:
            assignment = {
                'description': f'Assignment {j} for course: {course_code.strip()}', 
                'assignment_id': b,
                'calendar_event_id': random_event_id,
                'course_code': course_code.strip()
            }
            assignments.append({
                'description': assignment['description'],
                'calendar_event_id': assignment['calendar_event_id'],
                'course_code': assignment['course_code'],
                })
            course_assignments[course_code.strip()].append(assignment['assignment_id'])
            b=b+1
        elif j == 4:
            assignment = {
                'description': f'Mid-Term for course: {course_code.strip()}', 
                'assignment_id': b,
                'calendar_event_id': random_event_id,
                'course_code': course_code.strip()
            }
            assignments.append({
                'description': assignment['description'],
                'calendar_event_id': assignment['calendar_event_id'],
                'course_code': assignment['course_code'],
                })
            course_assignments[course_code.strip()].append(assignment['assignment_id'])
            b=b+1
        else:
            assignment = {
                'description': f'Final for course: {course_code.strip()}', 
                'assignment_id': b,
                'calendar_event_id': random_event_id,
                'course_code': course_code.strip()
            }
            assignments.append({
                'description': assignment['description'],
                'calendar_event_id': assignment['calendar_event_id'],
                'course_code': assignment['course_code'],
                })
            course_assignments[course_code.strip()].append(assignment['assignment_id'])
            b=b+1

print("Checkpoint 4")
# Loop through each student in the enrollment data
for student_id, student_data in student_enrollment_data.items():
    # Loop through each course that the student is enrolled in
    for course in student_data['courses']:
        if course['course_code'] in course_assignments:
            # Generate scores for each assignment for the current course
            for assignment_id in course_assignments[course['course_code']]:
                if 'scores' not in course:
                    course['scores'] = {}
                if 'student_submission' not in course:
                    course['student_submission'] = {}
                if assignment_id not in course['scores']:
                    course['scores'][assignment_id] = {}
                    course['student_submission'] [assignment_id]= {}
                # Check if the student already has a score for this assignment
                if student_id not in course['scores'][assignment_id]:
                    score = random.randint(50, 100)
                    student_submission = "Hello pretend I am the answer to the question!"
                    course['scores'][assignment_id][student_id] = score
                    course['student_submission'][assignment_id][student_id] = student_submission
a=0
print("Checkpoint 5")
for section in sections:
    a = a+1
    if section['section_name'] == 'Mid-Term Exam':
        course_content.append({
        'content_name': 'Mid-Term Exam',
        'content_description': 'This is your mid term examination for 2 hours',
        'section_id': a,
        })
        continue
    if section['section_name'] == 'Final Exam':
        course_content.append({
        'content_name': 'Final Exam',
        'content_description': 'This is your final examination for 1 hour',
        'section_id': a,
        })
        continue
    course_content.append({
        'content_name': 'Module 1',
        'content_description': 'Description for Module 1',
        'section_id': a,
        })
    course_content.append({
        'content_name': 'Module 2',
        'content_description': 'Description for Module 2',
        'section_id': a,
        })
    course_content.append({
        'content_name': 'Module 3',
        'content_description': 'Description for Module 3',
        'section_id': a,
        })
    course_content.append({
        'content_name': 'Module 4',
        'content_description': 'Description for Module 4',
        'section_id': a,
        })



print("***************Calandar Events***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/calendar_events.csv', mode='w', newline='') as csv_file:
    fieldnames = [ 'course_code', 'calendar_event_name', 'due_date', 'given_date'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for event in calendar_events:
        writer.writerow(event)

print("***************Forums***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/forum_posts.csv', mode='w', newline='') as csv_file:
    fieldnames = ['course_code', 'forum_name'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for forum in forum_posts:
        writer.writerow(forum)

print("***************Threads***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/threads.csv', mode='w', newline='') as csv_file:
    fieldnames = ['title', 'forum_id', 'message', 'account_id'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for discussion_thread in discussion_threads:
        writer.writerow(discussion_thread)

print("***************Thread Reply***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/thread_replies.csv', mode='w', newline='') as csv_file:
    fieldnames = ['title', 'thread_id', 'message', 'initial_message', 'account_id'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for reply in replies:
        writer.writerow(reply)

print("***************Sections***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sections.csv', mode='w', newline='') as csv_file:
    fieldnames = ['section_name', 'course_code'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for section in sections:
        writer.writerow(section)

print("***************Course Content***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/course_content.csv', mode='w', newline='') as csv_file:
    fieldnames = ['content_name', 'content_description', 'section_id'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for module in course_content:
        writer.writerow(module)

print("***************Assignments***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/assignments.csv', mode='w', newline='') as csv_file:
    fieldnames = ['description', 'calendar_event_id', 'course_code'] 
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for assignment in assignments:
        writer.writerow(assignment)

# Write grades to CSV file
print("***************Grades***************")
with open('C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/grades.csv', mode='w', newline='') as csv_file:
    fieldnames = ['score', 'student_submission', 'student_id', 'assignment_id']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    
    # Iterate over enrollment data for each student
    for student_id, student_data in student_enrollment_data.items():
        # Iterate over courses
        for course in student_data['courses']:
            course_code = course['course_code']
            scores = course['scores']
            student_submission = course['student_submission']
            # Iterate over scores for each course to extract assignment scores
            for assignment_id, score_dict in scores.items():
                score = score_dict.get(student_id)
                if score:
                    writer.writerow({'score': score,'student_submission':student_submission, 'student_id': student_id, 'assignment_id': assignment_id})