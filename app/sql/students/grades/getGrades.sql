SELECT a.description AS assignment_description, a.course_code, g.score,
       ac.first_name, ac.last_name, ac.email
FROM Grade g
JOIN Assignment a ON g.assignment_id = a.assignment_id
JOIN Student s ON g.student_id = s.student_id
JOIN Account ac ON s.account_id = ac.account_id
WHERE ac.username = :username
ORDER BY a.assignment_id;