-- use the database
-- use database_final_project;

-- create the Account table
CREATE TABLE IF NOT EXISTS Account (
    account_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    username BIGINT UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    email VARCHAR(256) UNIQUE NOT NULL,
    account_type INT NOT NULL
);

-- create the Admin table
CREATE TABLE IF NOT EXISTS Admin (
    admin_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT UNSIGNED,
    FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

-- create the Lecturer table
CREATE TABLE IF NOT EXISTS Lecturer (
    lecturer_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT UNSIGNED,
    FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

-- create the Course table
CREATE TABLE IF NOT EXISTS Course (
    course_code VARCHAR(16) PRIMARY KEY,
    course_name VARCHAR(256) NOT NULL,
    course_description VARCHAR(2056) NOT NULL,
    lecturer_id BIGINT UNSIGNED,
    FOREIGN KEY (lecturer_id) REFERENCES Lecturer (lecturer_id)
);

-- create the Student table
CREATE TABLE IF NOT EXISTS Student (
    student_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    account_id BIGINT UNSIGNED,
    FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

-- create the StudentCourses table
CREATE TABLE IF NOT EXISTS StudentCourse(
    course_code VARCHAR(16),
    student_id BIGINT UNSIGNED,
    FOREIGN KEY (course_code) REFERENCES Course(course_code),
    FOREIGN KEY (student_id) REFERENCES Student(student_id)
);


-- create the Section table
CREATE TABLE IF NOT EXISTS Section (
    section_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(256) NOT NULL,
    slides VARCHAR(128),
    links VARCHAR(128),
    files VARCHAR(128),
    course_code VARCHAR(16),
    FOREIGN KEY (course_code) REFERENCES Course (course_code)
);

-- create the Forum table
CREATE TABLE IF NOT EXISTS Forum (
    forum_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(16),
    FOREIGN KEY (course_code) REFERENCES Course (course_code)
);

-- create the CalendarEvent table
CREATE TABLE IF NOT EXISTS CalendarEvent (
    calendar_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    due_date DATE NOT NULL,
    given_date DATE NOT NULL
);

-- create the Assignment table
CREATE TABLE IF NOT EXISTS Assignment (
    assignment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(2056),
    calendar_event_id BIGINT UNSIGNED,
    course_code VARCHAR(16),
    FOREIGN KEY (calendar_event_id) REFERENCES CalendarEvent (calendar_event_id),
    FOREIGN KEY (course_code) REFERENCES Course (course_code)
);

-- create the Thread table
CREATE TABLE IF NOT EXISTS Thread (
    thread_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(256),
    forum_id BIGINT UNSIGNED,
    message VARCHAR(2056),
    initial_message BOOLEAN,
    account_id BIGINT UNSIGNED,
    FOREIGN KEY (forum_id) REFERENCES Forum (forum_id),
    FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

-- create the ThreadReply table
CREATE TABLE IF NOT EXISTS ThreadReply (
    thread_reply_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    thread_id BIGINT UNSIGNED,
    title VARCHAR(256),
    message VARCHAR(2056),
    initial_message BOOLEAN,
    account_id BIGINT UNSIGNED,
    FOREIGN KEY (thread_id) REFERENCES Thread (thread_id),
    FOREIGN KEY (account_id) REFERENCES Account (account_id)
);

-- create the Grade table
CREATE TABLE IF NOT EXISTS Grade (
    grade_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    score FLOAT,
    student_id BIGINT UNSIGNED,
    assignment_id BIGINT UNSIGNED,
    FOREIGN KEY (student_id) REFERENCES Student (student_id),
    FOREIGN KEY (assignment_id) REFERENCES Assignment (assignment_id)
);