SELECT c.course_code, c.course_name,  ac.first_name, ac.last_name, l.lecturer_id
FROM Student s 
JOIN studentcourse sc ON s.student_id = sc.student_id 
JOIN Course c ON c.course_code = sc.course_code 
LEFT JOIN Lecturer l ON c.lecturer_id = l.lecturer_id
LEFT JOIN Account ac ON ac.account_id = l.account_id
WHERE s.student_id = :student_id;