SELECT c.course_code, c.course_name 
FROM Student s 
JOIN studentcourse sc ON s.student_id = sc.student_id 
JOIN Course c ON c.course_code = sc.course_code 
WHERE s.student_id = :student_id;