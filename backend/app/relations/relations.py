from app.database import DatabaseConnection

# Returns true if the user is allowed to send the email
def email_allowed(userID, recipientID, senderID):
    
    # Check if the user is sending the email as themselves
    if userID != senderID:
        return False
    
    # Check if the recipient is in a relation with the sender
    sql = 'SELECT EXISTS (SELECT 1 FROM relation WHERE recipientID=%s AND senderID=%s)'
    data = (recipientID, senderID)
    conn = DatabaseConnection()
    with conn:
        exists = conn.execute(sql, data)
    if conn.error:
        return False
    
    if exists[0][0]:
        return True
