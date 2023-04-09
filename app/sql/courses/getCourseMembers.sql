SELECT Account.account_id, Account.first_name, Account.last_name, Account.username, Account.email, 'Lecturer' AS account_type
FROM Lecturer
JOIN Account ON Account.account_id = Lecturer.account_id
JOIN Course ON Course.lecturer_id = Lecturer.lecturer_id
WHERE Course.course_code = :course_code
UNION
SELECT Account.account_id, Account.first_name, Account.last_name, Account.username, Account.email, 'Student' AS account_type
FROM StudentCourse
JOIN Student ON Student.student_id = StudentCourse.student_id
JOIN Account ON Account.account_id = Student.account_id
JOIN Course ON Course.course_code = StudentCourse.course_code
WHERE Course.course_code = :course_code;