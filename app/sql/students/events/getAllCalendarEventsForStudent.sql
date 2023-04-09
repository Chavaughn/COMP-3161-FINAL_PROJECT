SELECT
  Course.course_code,
  CalendarEvent.calendar_event_name,
  CalendarEvent.due_date,
  CalendarEvent.given_date
FROM
  Account
  INNER JOIN Student ON Student.account_id = Account.account_id
  INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
  INNER JOIN Course ON StudentCourse.course_code = Course.course_code
  INNER JOIN CalendarEvent ON Course.course_code = CalendarEvent.course_code
WHERE
  Account.username = :username AND
  DATE(CalendarEvent.due_date) = :event_date