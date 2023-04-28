SELECT ac.*, l.lecturer_id, s.student_id
FROM Account ac
LEFT JOIN lecturer l ON l.account_id = ac.account_id
LEFT JOIN student s ON s.account_id = ac.account_id
LEFT JOIN admin ad ON ad.admin_id = ac.account_id
where username = :username;