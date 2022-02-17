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