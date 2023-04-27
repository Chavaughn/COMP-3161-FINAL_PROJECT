LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/enrollments.csv'
INTO TABLE StudentCourse
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(student_id,course_code);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/calendar_events.csv'
INTO TABLE CalendarEvent
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(course_code, calendar_event_name, due_date, given_date);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/forum_posts.csv'
INTO TABLE Forum
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(course_code, forum_name);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/threads.csv'
INTO TABLE Thread
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(title, forum_id, message, account_id);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/thread_replies.csv'
INTO TABLE ThreadReply
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(title, thread_id, message, initial_message, account_id);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sections.csv'
INTO TABLE Section
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(section_name, course_code);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/course_content.csv'
INTO TABLE CourseContent
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(content_name, content_description, section_id);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/assignments.csv'
INTO TABLE Assignment
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(description, calendar_event_id, course_code);

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/grades.csv'
INTO TABLE Grade
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(score, student_submission, student_id, assignment_id);

-- Add some links for FREN3001
INSERT INTO CourseLink (link_name, link_description, link_link, course_content_id)
VALUES 
    ('Link 1', 'Description of Link 1', 'https://www.link1.com', 1053),
    ('Link 2', 'Description of Link 2', 'https://www.link2.com', 1058),
    ('Link 3', 'Description of Link 3', 'https://www.link3.com', 1059),
    ('Link 4', 'Description of Link 4', 'https://www.link4.com', 1062),
    ('Link 5', 'Description of Link 5', 'https://www.link5.com', 1064);