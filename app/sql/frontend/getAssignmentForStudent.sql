SELECT a.*, ce.due_date as due_date, ce.given_date as given_date, g.score as score
FROM assignment a 
JOIN calendarevent ce ON a.calendar_event_id = ce.calendar_event_id 
LEFT JOIN grade g ON (g.assignment_id = a.assignment_id AND g.student_id = :student_id)
WHERE a.assignment_id = :assignment_id