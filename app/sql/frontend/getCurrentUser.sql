SELECT ac.* , st.student_id as student_id, lc.lecturer_id as lecturer_id
FROM Account ac
LEFT JOIN student st On st.account_id = ac.account_id 
LEFT JOIN lecturer lc On lc.account_id = ac.account_id 
WHERE ac.account_id = :account_id