from SoftwareEngProject.backend.app.messages.messages import send_message
from app.database import DatabaseConnection
from ../messages import messages
def create_meeting(relationshipID):
    conn = DatabaseConnection()
    # Check relationship exists and send request to mentor
    with conn:
        # Add to database
        sql = 'INSERT INTO message_meaning (menteeID, mentorID) VALUES (%s, %s)'
        data = (menteeID, mentorID)
        conn.execute(sql, data)
        send_message(mentorID, menteeID, "", sent_time)

    if conn.error:
        return (False, {'message': 'Meeting Request failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully requested'})

def cancel_meeting(meetingID):
    conn = DatabaseConnection()


def accept_meeting():
    conn = DatabaseConnection()

def get_meetings(ID, role):
    conn = DatabaseConnection()
    sql = "select * from meeting natural join relation where %s = %s;"
    # Either mentorid or menteeid
    data = (role + "id",ID)

    with DatabaseConnection() as conn:
        result = conn.execute(sql, data)
        if not conn.error:
            return result
        else:
            return None
