from app.database import DatabaseConnection

def get_messages(userID):
    sql = 'SELECT * FROM messages WHERE messageType = %s'
    data = (userID, )

    with DatabaseConnection() as conn:
        result = conn.execute(sql, data)
        if not conn.error:
            return result
        else:
            return None

# Returns true is message is successfully sent
def send_message(recipient, sender, message_type, contents):

    sql = 'INSERT INTO messages (recipient, sender, messageType, sentTime) VALUES (%s, %s, %s, %s)'
    data = (recipient, sender, message_type, contents)

    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
        
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, "")
