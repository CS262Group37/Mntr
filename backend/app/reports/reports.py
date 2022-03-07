from app.database import DatabaseConnection

def send_report()

def create_report(userID, contents):
    sql = 'INSERT INTO report (reportID, content, "status") VALUES (%s, %s, %s);'
    data = (userID, contents, "unread")

    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully create report'})

def send_report()