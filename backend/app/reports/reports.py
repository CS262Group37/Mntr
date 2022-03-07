from app.database import DatabaseConnection

def create_report(userID, contents):
    sql = 'INSERT INTO report (userID, content, "status") VALUES (%s, %s, %s);'
    data = (userID, contents, "unread")

    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully created report'})
# Send the report to all of the admins 

def mark_report_as_read(reportID):
    sql = "UPDATE report SET status = 'read' WHERE reportID = %s;"
    data = (reportID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully marked report as read'})

def get_report():
    sql = "SELECT * FROM report;"
    conn = DatabaseConnection()
    with conn:
        return conn.execute(sql)
    
