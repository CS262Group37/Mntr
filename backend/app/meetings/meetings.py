from datetime import datetime, timedelta
from time import time

from app.messages.messages import send_message, MeetingMessage
from app.database import DatabaseConnection

def str_to_datetime(str):
    try:
        datetime_object = datetime.strptime(str, '%d/%m/%y %H:%M')
    except:
        return False
    else:
        return datetime_object

# Create a new meeting
def create_meeting(relationID, start_time, end_time, title, description):
    conn = DatabaseConnection()
    # Check relationship exists and send request to mentor
    with conn:
        # Add to database
        sql = 'INSERT INTO meeting (relationID, startTime, endtime, title, "description", "status") VALUES (%s, %s, %s, %s, %s, \'pending\') RETURNING meetingID'
        data = (relationID, start_time, end_time, title, description)
        [(meetingID,)] = conn.execute(sql, data)
        sql = 'SELECT menteeID, mentorID FROM relation WHERE relationID=%s'
        data = (relationID,)
        [(menteeID, mentorID)] = conn.execute(sql, data)

        # Send meeting request
        meeting_message = MeetingMessage(mentorID, menteeID, 'request', meetingID)
        if not send_message(meeting_message):
            conn.error = True
            return (False, {'error': 'Failed to send meeting request.'})    
    
    if conn.error:
        return (False, {'message': 'Failed to create meeting', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully created'})

def get_meeting_relationID(meetingID):
    sql = 'SELECT relationID FROM meeting WHERE meetingID=%s'
    data = (meetingID,)
    conn = DatabaseConnection()
    with conn:
        relationID = conn.execute(sql, data)

    if not relationID:
        return None
    return relationID[0][0]

# Change a meeting to cancelled status
def cancel_meeting(meetingID):
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        sql = 'UPDATE meeting SET "status" = \'cancelled\' WHERE meetingID = %s;'
        data = (meetingID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting cancellation failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully cancelled'})

# Change a meeting to accepted status
def accept_meeting(meetingID):

    # Check meeting exists and then update to accept it
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        sql = 'UPDATE meeting SET "status" = \'going-ahead\' WHERE meetingID = %s;'
        data = (meetingID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting accept failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully accepted'})

# Updates all meetings in the database based on the current time
def update_meetings():

    sql = 'SELECT * FROM meeting'
    conn = DatabaseConnection()
    with conn:
        meetings = conn.execute(sql)
        current_time = datetime.now()

        sql = 'UPDATE meeting SET "status" = %s WHERE meetingID = %s'
        for meeting in meetings:
            
            start_time = meeting['starttime']
            print(f"TYPE OF START TIME IS {type(start_time)}")
            end_time = meeting['endtime']
            status = meeting['status']
            
            if status == 'cancelled' or status == 'completed':
                continue

            if current_time > end_time + datetime.timedelta(minutes=30):
                new_status = 'missed'
            elif current_time >= start_time and current_time <= end_time:
                new_status = 'running'

            if new_status != status:
                data = (new_status, meeting['meetingid'])
                conn.execute(sql, data)

    if conn.error:
        return False
    return True

# Gets all meetings for a user, regardless of status
def get_meetings(userID, role):
    update_meetings()

    if role == 'mentee':
        sql = "SELECT * FROM meeting NATURAL JOIN relation WHERE menteeID = %s;"
    else:
        sql = "SELECT * FROM meeting NATURAL JOIN relation WHERE mentorID = %s;"

    data = (userID,)
    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
        
    if conn.error:
        return None
    return result

# Mark meeting as completed and provide feedback
def complete_meeting(userID, meetingID, feedback):
    # Check meeting exists and then update to accept it
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        # You can only mark a meeting as completed if you are within 30 mins of the end time
        sql = 'SELECT endTime FROM meeting where meetingID = %s;'
        data = (meetingID,)
        [(end_time,)] = conn.execute(sql, data)
        if datetime.now() < end_time + timedelta(minutes=30): 
            sql = 'UPDATE meeting SET "status" = \'completed\', feedback = %s WHERE meetingID = %s;'
            data = (feedback, meetingID)
            conn.execute(sql, data)
        else:
            return (False, {'error': 'Cannot mark meeting as complete after 30 minutes.'})
        # Send meeting completed message
        # Get userIDs of meeting members
        sql = "SELECT (menteeID, mentorID) FROM meeting NATURAL JOIN relation WHERE meetingID = %s;"
        data = (meetingID,)
        [(menteeID, mentorID)] = conn.execute(sql, data)
        if menteeID is None or mentorID is None:
            conn.error = True
            return (False, {'error': 'Meeting does not exist'})
        if userID == menteeID:
            senderID = userID
            recipientID = mentorID
        else:
            senderID = mentorID
            recipientID = menteeID
        meeting_message = MeetingMessage(recipientID, mentorID, 'complete', meetingID)
        if not send_message(meeting_message):
            conn.error = True
            return (False, {'error': 'Failed to send meeting request.'}) 
    if conn.error:
        return (False, {'message': 'Meeting completion failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully completed'})
