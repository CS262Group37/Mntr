from app.database import DatabaseConnection

def create_report(userID, contents):
    sql = 'INSERT INTO report (reportID, content, "status") VALUES (%s, %s, %s);'
    data = (userID, contents, "unread")

    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully create report'})
# Send the report to all of the admins 

def mark_report_as_read(reportID):
    # TODO
