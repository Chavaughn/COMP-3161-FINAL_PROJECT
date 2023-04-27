SELECT Lecturer.lecturer_id, Account.username, Account.first_name, Account.last_name, COUNT(Course.course_code) AS course_count
FROM Account
INNER JOIN Lecturer ON Account.account_id = Lecturer.account_id
INNER JOIN Course ON Lecturer.lecturer_id = Course.lecturer_id
GROUP BY Account.first_name, Account.last_name
HAVING course_count >= 3;