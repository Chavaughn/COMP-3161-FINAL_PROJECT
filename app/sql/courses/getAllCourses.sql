SELECT c.course_code, c.course_name, c.course_description,  CONCAT(ac.first_name, " " ,ac.last_name) as lecturer_name, COUNT(sc.student_id) as students
FROM course c
LEFT JOIN lecturer lc on lc.lecturer_id = c.lecturer_id
LEFT JOIN account ac on ac.account_id = lc.lecturer_id
LEFT JOIN studentcourse sc ON sc.course_code = c.course_code
group by c.course_code
ORDER BY students;