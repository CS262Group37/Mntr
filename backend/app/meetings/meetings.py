from SoftwareEngProject.backend.app.messages.messages import send_message
from app.database import DatabaseConnection
from app.messages import messages

# Create a new meeting
def create_meeting(relationshipID, start_time, duration, title, description):
    conn = DatabaseConnection()
    # Check relationship exists and send request to mentor
    with conn:
        # Add to database
        sql = 'INSERT INTO meeting (relationID, startTime, duration, title, descript, _status) VALUES (%s, %s, %s, %s, %s, "pending")'
        data = (relationshipID, start_time, duration, title,description)
        conn.execute(sql, data)
        # send_message(mentorID, menteeID, "", sent_time)

    if conn.error:
        return (False, {'message': 'Meeting Request failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully created'})

# Change a meeting to cancelled status
def cancel_meeting(meetingID):
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        sql = 'UPDATE meeting SET _status = "cancelled" WHERE meetingID = %s;'
        data = (meetingID)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting cancellation failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully cancelled'})

# Change a meeting to accepted status
def accept_meeting(meetingID):
    conn = DatabaseConnection()
    # Check meeting exists and then update to accept it
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        sql = 'UPDATE meeting SET _status = "accept" WHERE EXISTS (SELECT * FROM meeting WHERE meetingID = %s);'
        data = (meetingID)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting accept failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully accepted'})

# Gets all meetings for a user, regardless of status
def get_all_meetings(ID, role):
    conn = DatabaseConnection()
    if role == 'mentee':
        sql = "select * from meeting natural join relation where menteeID = %s;"
    else:
        sql = "select * from meeting natural join relation where mentorID = %s;"

    data = (ID)

    with DatabaseConnection() as conn:
        result = conn.execute(sql, data)
        if not conn.error:
            return result
        else:
            return None

# Gets all accepted meetings for the user
def get_accepted_meetings(ID, role):
    return get_x_meetings(ID,role,"accepted")

# Gets all pending meetings for the user
def get_pending_meetings(ID,role):
    return get_x_meetings(ID,role,"pending")

# Gets all cancelled meetings for the user
def get_cancelled_meetings(ID,role):
    return get_x_meetings(ID,role,"pending")



# Gets meetings for the user with a specific status
def get_x_meetings(ID,role,get_type):
    conn = DatabaseConnection()
    # Decided whether to find based on mentee or mentor ids
    if role == 'mentee':
        sql = "select * from meeting natural join relation where menteeID = %s and _status = %s;"
    else:
        sql = "select * from meeting natural join relation where mentorID = %s and _status = %s;"
    # Fill in the query with the id and status type
    data = (ID, get_type)

    with DatabaseConnection() as conn:
        result = conn.execute(sql, data)
        if not conn.error:
            return result
        else:
            return None