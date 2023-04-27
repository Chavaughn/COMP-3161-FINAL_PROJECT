SELECT Course.course_code, Course.course_name, COUNT(StudentCourse.student_id) AS student_count
FROM Course
INNER JOIN StudentCourse ON Course.course_code = StudentCourse.course_code
GROUP BY Course.course_code, Course.course_name
ORDER BY student_count DESC
LIMIT 10;