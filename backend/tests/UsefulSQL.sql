-- Get login details for a given userID
SELECT * FROM "user" NATURAL JOIN account WHERE userID = 15;

SELECT 
    * 
FROM message 
LEFT JOIN 
    message_meeting 
    ON message.messageID = message_meeting.messageID 
LEFT JOIN message_email
    ON message.messageID = message_email.messageID    
WHERE recipientID = 3;