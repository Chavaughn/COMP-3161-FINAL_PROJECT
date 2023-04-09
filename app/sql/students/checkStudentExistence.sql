SELECT EXISTS(SELECT 1 FROM Student 
              INNER JOIN Account ON Student.account_id = Account.account_id 
              WHERE Account.username = :username AND Account.account_type = 3)