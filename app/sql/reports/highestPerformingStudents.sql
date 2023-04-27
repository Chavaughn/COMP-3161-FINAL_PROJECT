SELECT 
  Student.student_id, 
  ac.username,
  ac.first_name, 
  ac.last_name, 
  AVG(Grade.score) AS final_average
FROM 
  Student 
  INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
  INNER JOIN Course ON StudentCourse.course_code = Course.course_code
  INNER JOIN Assignment ON Course.course_code = Assignment.course_code
  INNER JOIN Grade ON Assignment.assignment_id = Grade.assignment_id AND Student.student_id = Grade.student_id
  INNER JOIN Account AS ac ON Student.account_id = ac.account_id
GROUP BY 
  Student.student_id
ORDER BY 
  final_average DESC 
LIMIT 
  10;
