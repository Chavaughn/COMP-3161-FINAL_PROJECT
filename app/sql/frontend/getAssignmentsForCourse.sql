SELECT a.*, ce.due_date as due_date, ce.given_date as given_date
FROM assignment a 
JOIN calendarevent ce ON a.calendar_event_id = ce.calendar_event_id 
WHERE a.course_code = :course_code
ORDER BY ce.due_date;