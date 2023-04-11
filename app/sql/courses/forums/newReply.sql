INSERT INTO ThreadReply 
(thread_id, title, message, parent_reply_id, initial_message, account_id)
 VALUES
  (:thread_id, :title, :message, :parent_reply_id, :initial_message, :account_id);