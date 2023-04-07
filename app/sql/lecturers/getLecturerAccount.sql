SELECT a.account_id, a.first_name, a.last_name, a.username, a.password, a.email, a.account_type
FROM Lecturer l 
JOIN Account a ON l.account_id = a.account_id 
WHERE l.lecturer_id = :lecturer_id;