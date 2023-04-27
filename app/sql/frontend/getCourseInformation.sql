-- Course, Lecturer's account first name and last name, sections[course content[slides, link, file], forum[thread[threadreplies]], calendar event[assignment[grade]]]
SELECT c.course_code, c.course_name, c.course_description, ac.first_name, ac.last_name
FROM
course as c
LEFT JOIN lecturer l on l.lecturer_id = c.lecturer_id
LEFT JOIN account ac on l.account_id = ac.account_id
WHERE c.course_code = :course_code