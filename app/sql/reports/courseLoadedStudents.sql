SELECT Student.student_id, Account.username, Account.first_name, Account.last_name, COUNT(DISTINCT StudentCourse.course_code) AS course_count
FROM Account
INNER JOIN Student ON Account.account_id = Student.account_id
INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
GROUP BY Account.first_name, Account.last_name
HAVING course_count >= 5;